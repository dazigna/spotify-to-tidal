from ssl import SSLContext, PROTOCOL_TLS_SERVER
from multidict._multidict_py import MultiDictProxy

from http.server import HTTPServer

from yarl import URL
from http import server
from loguru import logger
from common.config_manager import ConfigManager
from common.network_manager import NetworkManager
from common.storage import Storage
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
        self.storage: Storage = kwargs.pop("storage")
        # self.config_manager: ConfigManager = config_manager
        # self.network_manager: NetworkManager = network_manager
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # try:
        #     url = URL(self.path)
        # except ValueError:
        #     print(f"{self.path=}")
        url = URL(self.path)
        logger.info(f"Received incoming request: {url}, {url.path}, {url.query}")

        if url.path == "/auth/spotify/callback":
            params: MultiDictProxy[str] = url.query
            auth_code: str | None = params.get("code")
            state: str | None = params.get("state")
            error: str | None = params.get("error")
            logger.info(f"parameters extracted {auth_code}, {state}, {error}")
            # now get the access token
            if auth_code and state and not error:
                _ = Authenticator(
                    config_manager=self.config_manager,
                    network_manager=self.network_manager,
                    storage=self.storage,
                ).request_access_token(code=auth_code, state=state)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                _ = self.wfile.write(
                    b"Authentication successful! You can close this window."
                )
            elif error:
                logger.error(f"Error: {error}")
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                _ = self.wfile.write(b"Authentication failed.")
            else:
                logger.error("Error: No parameters extracted")
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                _ = self.wfile.write(b"request failed - nothing extracted")

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
        storage: Storage,
        # request_handler_class: type[server.BaseHTTPRequestHandler],
        host: str = "127.0.0.1",
        port: int = 3000,
    ):
        self.port: int = port
        self.host: str = host
        self.server_address: tuple[str, int] = (self.host, self.port)
        self.config_manager: ConfigManager = config_manager
        self.network_manager: NetworkManager = network_manager
        self.storage: Storage = storage

        def handler(*args, **kwargs):
            kwargs["config_manager"] = self.config_manager
            kwargs["network_manager"] = self.network_manager
            kwargs["storage"] = self.storage
            return SimpleServerRequestHandler(*args, **kwargs)

        # Create an SSL context
        self.context: SSLContext = SSLContext(PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(config_manager.cert_file, config_manager.key_file)

        self.httpd: HTTPServer = server.HTTPServer(self.server_address, handler)
        # Wrap the socket with the SSL context
        self.httpd.socket = self.context.wrap_socket(
            self.httpd.socket, server_side=True
        )

    def serve(self):
        self.httpd.serve_forever()

    def shutdown(self):
        self.httpd.shutdown()
