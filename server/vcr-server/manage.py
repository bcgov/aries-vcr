#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vcr_server.settings")

    from django.conf import settings

    if settings.DJANGO_DEBUG:
        if os.environ.get("RUN_MAIN") or os.environ.get("WERKZEUG_RUN_MAIN"):
            import debugpy

            debugpy.listen(("0.0.0.0", 3000))
            print("Remote debugger listening on port 3000")
            debugpy.wait_for_client()  # blocks execution until client is attached
            print("Remote debugger attached")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
