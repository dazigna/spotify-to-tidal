from http.server import HTTPServer

from ada_url import parse_search_params
from http import server
from loguru import logger
from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from spotify.authenticator import Authenticator


class SimpleServerRequestHandler(server.BaseHTTPRequestHandler):
    def __init__(
        self,
        # config_manager: ConfigManager,
        # network_manager: NetworkManager,
        *args,
        **kwargs,
    ) -> None:
        self.config_manager: ConfigManager = kwargs.pop("config_manager")
        self.network_manager: NetworkManager = kwargs.pop("network_manager")
        # self.config_manager: ConfigManager = config_manager
        # self.network_manager: NetworkManager = network_manager
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # try:
        #     url = URL(self.path)
        # except ValueError:
        #     print(f"{self.path=}")

        if self.path == "auth/spotify/callback":
            # TODO: Fix this - ada library seems shit.
            params = parse_search_params(url.search)
            auth_code: str | None = params.get("code", [None])[0]
            state: str | None = params.get("state", [None])[0]
            error: str | None = params.get("error", [None])[0]
            # now get the access token
            if auth_code and state:
                _ = Authenticator(
                    config_manager=self.config_manager,
                    network_manager=self.network_manager,
                ).request_access_token(code=auth_code, state=state)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                _ = self.wfile.write(
                    b"Authentication successful! You can close this window."
                )

            if error:
                logger.error(f"Error: {error}")
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                _ = self.wfile.write(b"Authentication failed.")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            _ = self.wfile.write(b"Not found - 404.")


class SimpleAuthServer:
    def __init__(
        self,
        config_manager: ConfigManager,
        network_manager: NetworkManager,
        # request_handler_class: type[server.BaseHTTPRequestHandler],
        host: str = "localhost",
        port: int = 3000,
    ):
        self.port: int = port
        self.host: str = host
        self.server_address: tuple[str, int] = (self.host, self.port)
        self.config_manager: ConfigManager = config_manager
        self.network_manager: NetworkManager = network_manager

        def handler(*args, **kwargs):
            kwargs["config_manager"] = self.config_manager
            kwargs["network_manager"] = self.network_manager
            return SimpleServerRequestHandler(*args, **kwargs)

        self.httpd: HTTPServer = server.HTTPServer(self.server_address, handler)

    def serve(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()
