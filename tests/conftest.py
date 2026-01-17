import http.server
import os
import re
import socketserver
import sys
import threading
from functools import partial
from pathlib import Path

import nest_asyncio
import pytest
from pyodide_version_mapping import PYODIDE_TO_PYTHON_VERSIONS

# Add src directory to sys.path to allow importing pyodide_app
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Existing Pyodide version fixtures


def pytest_addoption(parser):
    """Add a command line option to specify the Pyodide version."""
    parser.addoption(
        "--pyodide-version",
        action="store",
        default="0.28.0",
        help="Specify the Pyodide version to test against.",
    )


@pytest.fixture(scope="session")
def pyodide_version(request):
    """Return the Pyodide version specified on the command line."""
    return request.config.getoption("--pyodide-version")


def pytest_configure(config):
    """
    Validate that the local Python version matches the required version
    for the selected Pyodide version.
    """
    nest_asyncio.apply()
    pyodide_version = config.getoption("--pyodide-version")
    if pyodide_version not in PYODIDE_TO_PYTHON_VERSIONS:
        pytest.exit(f"Unknown Pyodide version: {pyodide_version}", returncode=1)

    required_python_version = PYODIDE_TO_PYTHON_VERSIONS[pyodide_version]
    current_python_version = ".".join(map(str, sys.version_info[:3]))

    if not current_python_version.startswith(required_python_version.rsplit(".", 1)[0]):
        print(
            f"WARNING: Pyodide version {pyodide_version} requires Python "
            f"{required_python_version}, but the local version is "
            f"{current_python_version}. Proceeding anyway."
        )
        # pytest.exit(
        #     f"Pyodide version {pyodide_version} requires Python "
        #     f"{required_python_version}, "
        #     f"but the local version is {current_python_version}.",
        #     returncode=1,
        # )


# New HTTP server fixtures (with and without CORS)


class CorsHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that sends permissive CORS headers for cross‑origin requests."""

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        return super().end_headers()


class NoCorsHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that does **not** send CORS headers (default behavior)."""

    pass


@pytest.fixture(scope="session")
def live_server(pyodide_version):
    """
    A robust, threaded HTTP server that serves the pyodide-patterns directory.
    It dynamically injects the correct Pyodide version into index.html by
    serving a modified version from memory.
    It also sends CORS headers.
    """
    project_root = Path(__file__).parent.parent
    original_index_html_path = project_root / "index.html"

    # Read and modify the index.html content in memory
    pattern = re.compile(r"https://cdn.jsdelivr.net/pyodide/v[^/]+/full/pyodide.js")
    new_url = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/pyodide.js"

    if not original_index_html_path.exists():
        pytest.fail(f"index.html not found at {original_index_html_path}")

    original_content = original_index_html_path.read_text(encoding="utf-8")
    if not pattern.search(original_content):
        print(
            f"WARNING: Could not find Pyodide CDN URL in "
            f"{original_index_html_path} to replace."
        )
        modified_content_bytes = original_content.encode("utf-8")
    else:
        modified_content_bytes = pattern.sub(new_url, original_content).encode("utf-8")

    class PyodideHandler(CorsHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(project_root), **kwargs)

        def do_GET(self):
            if self.path == "/index.html" or self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length", str(len(modified_content_bytes)))
                self.end_headers()
                self.wfile.write(modified_content_bytes)
            else:
                super().do_GET()

    with socketserver.TCPServer(("localhost", 0), PyodideHandler) as httpd:
        host, port = httpd.server_address
        base_url = f"http://{host}:{port}"
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        yield base_url
        httpd.shutdown()
        server_thread.join()


@pytest.fixture(scope="session")
def cross_origin_server():
    """Start a second HTTP server **without** CORS headers.
    Used to test CORS‑related failure scenarios."""
    web_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    handler = partial(NoCorsHandler, directory=web_root)
    with socketserver.TCPServer(("localhost", 0), handler) as httpd:
        host, port = httpd.server_address
        base_url = f"http://{host}:{port}"
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        yield base_url
        httpd.shutdown()
        server_thread.join()


@pytest.fixture(scope="session")
def http_server(live_server):
    """Alias for live_server to support ported tests."""
    return live_server
