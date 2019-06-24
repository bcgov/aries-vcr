import asyncio
import json
import os
import random
import subprocess

from aiohttp import web, ClientSession, ClientRequest, ClientError
import colored

COLORIZE = os.environ.get("TERM") == "xterm"


def print_color(msg, color, prefix="", end=None):
    if color and COLORIZE:
        msg = colored.stylize(msg, colored.fg(color))
    if prefix:
        msg = f"{prefix:10s} | {msg}"
    print(msg, end=end)


def output_reader(handle, callback, loop, *args, **kwargs):
    for line in iter(handle.readline, b""):
        if not line:
            break
        asyncio.run_coroutine_threadsafe(callback(line, *args), loop)


def flatten(args):
    for arg in args:
        if isinstance(arg, (list, tuple)):
            yield from flatten(arg)
        else:
            yield arg


class DemoAgent:
    def __init__(
        self,
        ident: str,
        http_port: int,
        admin_port: int,
        internal_host: str,
        external_host: str,
        label: str = None,
        timing: bool = False,
        postgres: bool = False,
        **params,
    ):
        self.ident = ident
        self.http_port = http_port
        self.admin_port = admin_port
        self.internal_host = internal_host
        self.external_host = external_host
        self.label = label or ident
        self.timing = timing
        self.postgres = postgres

        self.endpoint = f"http://{internal_host}:{http_port}"
        self.admin_url = f"http://{internal_host}:{admin_port}"
        self.webhook_port = None
        self.webhook_url = None
        self.params = params
        self.proc = None
        self.wh_site = None
        self.client_session: ClientSession = ClientSession()

        rand_name = str(random.randint(100_000, 999_999))
        self.seed = (
            params.get("seed") or ("my_seed_000000000000000000000000" + rand_name)[-32:]
        )
        self.storage_type = params.get("storage_type")
        self.wallet_type = params.get("wallet_type", "indy")
        self.wallet_name = params.get("wallet_name") or self.ident.lower() + rand_name
        self.wallet_key = params.get("wallet_key") or self.ident + rand_name
        self.did = None

    def get_agent_args(self):
        result = [
            ("--endpoint", self.endpoint),
            ("--label", self.label),
            "--auto-respond-messages",
            "--accept-invites",
            "--accept-requests",
            "--auto-ping-connection",
            "--auto-respond-credential-offer",
            "--auto-respond-presentation-request",
            ("--inbound-transport", "http", "0.0.0.0", str(self.http_port)),
            ("--outbound-transport", "http"),
            ("--admin", "0.0.0.0", str(self.admin_port)),
            ("--wallet-type", self.wallet_type),
            ("--wallet-name", self.wallet_name),
            ("--wallet-key", self.wallet_key),
            ("--seed", self.seed),
        ]
        if "genesis" in self.params:
            result.append(("--genesis-transactions", self.params["genesis"]))
        if self.storage_type:
            result.append(("--storage-type", self.storage_type))
        if self.timing:
            result.append("--timing")
        if self.postgres:
            result.extend(
                [
                    ("--wallet-storage-type", "postgres_storage"),
                    (
                        "--wallet-storage-config",
                        json.dumps(
                            {
                                "url": f"{self.internal_host}:5432",
                                "tls": "None",
                                "max_connections": 5,
                                "min_idle_time": 0,
                                "connection_timeout": 10,
                            }
                        ),
                    ),
                    (
                        "--wallet-storage-creds",
                        json.dumps(
                            {
                                "account": "postgres",
                                "password": "mysecretpassword",
                                "admin_account": "postgres",
                                "admin_password": "mysecretpassword",
                            }
                        ),
                    ),
                ]
            )

        return result

    async def register_did(self, ledger_url=None):
        self.log(f"Registering {self.ident} with seed {self.seed}")
        if not ledger_url:
            ledger_url = f"http://{self.external_host}:9000"
        data = {"alias": self.ident, "seed": self.seed, "role": "TRUST_ANCHOR"}
        async with self.client_session.post(
            ledger_url + "/register", json=data
        ) as resp:
            if resp.status != 200:
                raise Exception(f"Error registering DID, response code {resp.status}")
            nym_info = await resp.json()
            self.did = nym_info["did"]
        self.log(f"Got DID: {self.did}")

    async def handle_output(self, output, source=""):
        end = "" if source else "\n"
        if source == "stderr" and COLORIZE:
            color = "red"
        elif not source and COLORIZE:
            color = "blue"
        else:
            color = None
        print_color(output, color, self.ident, end=end)

    def log(self, msg, *, loop=None):
        asyncio.run_coroutine_threadsafe(
            self.handle_output(msg), loop or asyncio.get_event_loop()
        )

    def _process(self, args, env, loop):
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            encoding="utf-8",
        )
        loop.run_in_executor(
            None, output_reader, proc.stdout, self.handle_output, loop, "stdout"
        )
        loop.run_in_executor(
            None, output_reader, proc.stderr, self.handle_output, loop, "stderr"
        )
        return proc

    def get_process_args(self, scripts_dir: str):
        return list(
            flatten((["python3", scripts_dir + "icatagent"], self.get_agent_args()))
        )

    async def start_process(
        self, python_path="..", scripts_dir="../scripts/", wait=True
    ):
        my_env = os.environ.copy()
        my_env["PYTHONPATH"] = python_path

        # refer to REST callback service
        if self.webhook_url:
            my_env["WEBHOOK_URL"] = self.webhook_url

        agent_args = self.get_process_args(scripts_dir)

        # start agent sub-process
        loop = asyncio.get_event_loop()
        self.proc = await loop.run_in_executor(
            None, self._process, agent_args, my_env, loop
        )
        if wait:
            await self.detect_process()

    def _terminate(self, loop):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=0.5)
                self.log(f"Exited with return code {self.proc.returncode}", loop=loop)
            except subprocess.TimeoutExpired:
                msg = "Process did not terminate in time"
                self.log(msg, loop=loop)
                raise Exception(msg)

    async def terminate(self):
        loop = asyncio.get_event_loop()
        if self.proc:
            await loop.run_in_executor(None, self._terminate, loop)
        await self.client_session.close()
        if self.wh_site:
            await self.wh_site.stop()

    async def listen_webhooks(self, webhook_port):
        self.webhook_port = webhook_port
        self.webhook_url = f"http://{self.external_host}:{str(webhook_port)}/webhooks"
        app = web.Application()
        app.add_routes([web.post("/webhooks/topic/{topic}/", self._receive_webhook)])
        runner = web.AppRunner(app)
        await runner.setup()
        self.wh_site = web.TCPSite(runner, "0.0.0.0", webhook_port)
        await self.wh_site.start()

    async def _receive_webhook(self, request: ClientRequest):
        topic = request.match_info["topic"]
        payload = await request.json()
        await self.handle_webhook(topic, payload)
        return web.HTTPOk()

    async def handle_webhook(self, topic: str, payload):
        pass

    async def admin_GET(self, path, text=False):
        async with self.client_session.get(self.admin_url + path) as resp:
            return await (resp.text() if text else resp.json())

    async def admin_POST(self, path, data=None, text=False):
        async with self.client_session.post(self.admin_url + path, json=data) as resp:
            return await (resp.text() if text else resp.json())

    async def detect_process(self):
        text = None
        for i in range(10):
            # wait for process to start and retrieve swagger content
            await asyncio.sleep(2.0)
            try:
                async with self.client_session.get(
                    self.admin_url + "/api/docs/swagger.json"
                ) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        break
            except ClientError:
                text = None
                continue
        if not text:
            raise Exception(f"Timed out waiting for agent process to start")
        if "Indy Catalyst Agent" not in text:
            raise Exception(f"Unexpected response from agent process")

    async def fetch_timing(self):
        status = await self.admin_GET("/status")
        return status.get("timing")

    def format_timing(self, timing: dict) -> dict:
        result = []
        for name, count in timing["count"].items():
            result.append(
                (
                    name[:35],
                    count,
                    timing["total"][name],
                    timing["avg"][name],
                    timing["min"][name],
                    timing["max"][name],
                )
            )
        result.sort(key=lambda row: row[2], reverse=True)
        yield "{:35} | {:>12} {:>12} {:>10} {:>10} {:>10}".format(
            "", "count", "total", "avg", "min", "max"
        )
        yield "=" * 96
        yield from (
            "{:35} | {:12d} {:12.3f} {:10.3f} {:10.3f} {:10.3f}".format(*row)
            for row in result
        )

    async def reset_timing(self):
        await self.admin_POST("/status/reset", text=True)
