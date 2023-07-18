import locale
import sys

from paste import httpserver

from host.app import application


def main():
    """Main logic."""

    # Set the locale to the system one for number formatting
    locale.setlocale(locale.LC_ALL, "")

    httpserver.serve(application, host="0.0.0.0", port=9999)


if __name__ == "__main__":
    sys.exit(main())
