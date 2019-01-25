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


def print_start_banner(transports):

    banner_length = 40

    banner_title_string = "Indy Catalyst Agent"
    banner_title_spacer = " " * (banner_length - len(banner_title_string))

    banner_border = ":" * (banner_length + 6)
    banner_spacer = "::" + " " * (banner_length + 2) + "::"

    interfaces_subtitle_string = "Inferfaces:"
    interfaces_subtitle_spacer = " " * (banner_length - len(interfaces_subtitle_string))

    transport_strings = []
    for transport in transports:
        host_port_string = f"{transport.module}: {transport.host}:{transport.port}"
        host_port_spacer = " " * (banner_length - len(host_port_string))
        transport_strings.append((host_port_string, host_port_spacer))

    version_string = f"ver: {__version__}"
    version_string_spacer = " " * (banner_length - len(version_string))

    print()
    print(f"{banner_border}")
    print(f":: {banner_title_string}{banner_title_spacer} ::")
    print(f"{banner_spacer}")
    print(f"{banner_spacer}")
    print(f":: {interfaces_subtitle_string}{interfaces_subtitle_spacer} ::")
    print(f"{banner_spacer}")
    for transport_string in transport_strings:
        print(f":: {transport_string[0]}{transport_string[1]} ::")
    print(f"{banner_spacer}")
    print(f":: {version_string_spacer}{version_string} ::")
    print(f"{banner_border}")
    print()
    print("Listening...")
    print()


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

    print_start_banner(transport_configs)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start(transport_configs))
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nShutting down")


if __name__ == "__main__":
    main()  # pragma: no cover
