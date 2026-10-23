"""Serve the viewer/ directory over plain HTTP and open a browser.

ES module imports and fetch() for data/points.ply both require a real HTTP
origin (file:// breaks module resolution and CORS), so this step is required,
not cosmetic.
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import threading
import webbrowser


def serve(viewer_dir: str, port: int = 8000, open_browser: bool = True) -> None:
    # extensions_map is a class attribute (shared dict), not settable on the
    # functools.partial wrapper below — mutate it on the class itself first.
    http.server.SimpleHTTPRequestHandler.extensions_map.setdefault(".ply", "application/octet-stream")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=viewer_dir)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving hologram viewer at {url}  (Ctrl+C to stop)")

        if open_browser:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
