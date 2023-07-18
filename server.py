"""
Local web server for testing purposes.
"""

if __name__ == "__main__":
    from paste import httpserver

    from host.app import application

    httpserver.serve(application, host="0.0.0.0", port=9999)
