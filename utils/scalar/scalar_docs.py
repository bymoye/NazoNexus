from blacksheep.server.openapi.ui import (
    UIFilesOptions,
    UIProvider,
    UIOptions,
)
from typing import Callable
from blacksheep import Request, Response, moved_permanently
from blacksheep.utils.time import utcnow
from blacksheep.server.files.static import get_response_for_static_content
from blacksheep.server.resources import get_resource_file_path

SCALAR_UI_JS_URL = "https://registry.npmmirror.com/@scalar/api-reference/1.28.17/files/dist/browser/standalone.js"
SCALAR_UI_CSS_URL = (
    "https://registry.npmmirror.com/@scalar/api-reference/1.28.17/files/dist/style.css"
)
SCALAR_UI_FONT = None


class ScalarUIProvider(UIProvider):
    """
    UI provider for Scalar API Reference.
    Scalar is a modern, interactive API documentation tool.
    """

    def __init__(
        self, ui_path: str = "/scalar", ui_files: UIFilesOptions | None = None
    ) -> None:
        super().__init__(ui_path, ui_files)

        self._ui_html: bytes = b""

    def get_openapi_ui_html(self, options: UIOptions) -> str:
        """
        Returns the HTML response to serve the Scalar API Reference UI.
        Parameters:
        options (UIOptions): Configuration options for the UI
        Returns:
        str: HTML content for the Scalar UI
        """
        with open(
            get_resource_file_path("utils.scalar", "scalar_ui.html"), mode="rt"
        ) as source:
            return (
                source.read()
                .replace("##PAGE_TITLE##", options.page_title)
                .replace("##FAVICON_URL##", options.favicon_url)
                .replace("##CSS_URL##", self.ui_files.css_url or "")
                .replace("##SPEC_URL##", options.spec_url)
                .replace("##JS_URL##", self.ui_files.js_url or "")
            )

    def build_ui(self, options: UIOptions) -> None:
        """
        Prepares the UI that will be served by the UI route.
        Parameters:
        options (UIOptions): Configuration options for the UI
        """
        self._ui_html = self.get_openapi_ui_html(options).encode("utf8")

    def get_ui_handler(self) -> Callable[[Request], Response]:
        """
        Returns a request handler for the route that serves the Scalar UI.
        Returns:
        Callable: Request handler function
        """
        current_time = utcnow().timestamp()

        def get_open_api_ui(request: Request) -> Response:
            path = request.path

            if not path.endswith("/"):
                return moved_permanently(f"/{path.strip('/')}/")

            return get_response_for_static_content(
                request, b"text/html; charset=utf-8", self._ui_html, current_time
            )

        return get_open_api_ui

    @property
    def default_ui_files(self) -> UIFilesOptions:
        """
        Returns the default UI files options for Scalar.
        Returns:
        UIFilesOptions: Default CDN URLs for Scalar UI
        """
        return UIFilesOptions(SCALAR_UI_JS_URL, SCALAR_UI_CSS_URL, SCALAR_UI_FONT)
