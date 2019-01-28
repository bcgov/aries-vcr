import argparse
import asyncio
import signal

from .conductor import Conductor
from .logging import LoggingConfigurator
from .transport.inbound import InboundTransportConfiguration

from .version import __version__


parser = argparse.ArgumentParser(description="Runs an Indy Agent.")

parser.add_argument(
    "--transport",
    dest="transports",
    type=str,
    action="append",
    nargs=3,
    required=True,
    metavar=("<module>", "<host>", "<port>"),
    help="Choose which interface(s) to listen on",
)

parser.add_argument(
    "--logging-config",
    dest="logging_config",
    type=str,
    metavar="<path-to-config>",
    default=None,
    help="Specifies a custom logging configuration file",
)


async def start(transport_configs):
    conductor = Conductor(transport_configs)
    await conductor.start()


def main():
    args = parser.parse_args()

    transport_configs = []

    transports = args.transports
    for transport in transports:
        module = transport[0]
        host = transport[1]
        port = transport[2]
        transport_configs.append(
            InboundTransportConfiguration(module=module, host=host, port=port)
        )

    logging_config = args.logging_config
    LoggingConfigurator.configure(logging_config)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start(transport_configs))
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nShutting down")


if __name__ == "__main__":
    main()  # pragma: no cover
