import json
import logging
import os
from typing import Any, Coroutine

import httpx
from urllib3.util.url import Url, parse_url

logger = logging.getLogger(__name__)

LUMOS_PROXY_HOST = os.environ.get("LUMOS_PROXY_HOST", None)
LUMOS_PROXY_HEADERS = httpx.Headers(json.loads(os.environ.get("LUMOS_PROXY_HEADERS", "{}")))


def set_proxy_host(host: str | None = None) -> None:
    """
    Set the proxy host for all httpx_rewrite.AsyncClient requests.

    If host is None, requests will no longer be proxied, until and unless
    the host is set to a valid host.
    """
    global LUMOS_PROXY_HOST
    LUMOS_PROXY_HOST = host


def add_proxy_headers(headers: dict[str, str]) -> None:
    """
    Add any passed-in headers to a global set of headers sent on proxied requests.

    These will only be used if the proxy host is set.
    """
    global LUMOS_PROXY_HEADERS
    for header_name, header_value in headers.items():
        LUMOS_PROXY_HEADERS[header_name] = header_value


class AsyncClient(httpx.AsyncClient):
    """
    A slightly modified version of httpx.AsyncClient, that may rewrite requests to go to a proxy.

    Requests will be rewritten if either of these is true
    - The env var LUMOS_PROXY_HOST is set (e.g. to http://my-proxy:4444)
    - this module's function `set_proxy_host` is called with a new host

    Rewritten requests...
    1. will go to the proxy host's domain, with path `/proxy`.
    2. will have the original request line (including fragment) preserved in the header `X-Forward-To`
    3. will have their headers preserved, EXCEPT FOR...
       a. `Host` will be set to the proxy host
       b. Additional headers will be set, and overwrite any passed-in headers, from
         - the LUMOS_PROXY_HEADERS environment variable (as JSON)
         - the accumulated calls to this module's `add_proxy_headers` function
    """

    def will_rewrite_request(self) -> bool:
        return bool(LUMOS_PROXY_HOST)

    def send(self, request: httpx.Request, **kwargs) -> Coroutine[Any, Any, httpx.Response]:
        if LUMOS_PROXY_HOST:
            logger.debug("Proxying all requests to %s", LUMOS_PROXY_HOST)
            override = parse_url(LUMOS_PROXY_HOST)
            self.proxy_headers = LUMOS_PROXY_HEADERS
        else:
            return super(AsyncClient, self).send(request, **kwargs)

        # Update request URL
        url = str(request.url)
        updated = Url(
            scheme=override.scheme,
            host=override.host,
            port=override.port,
            path="/proxy",
        )

        # Rewrite headers
        new_headers = request.headers.copy()
        new_headers["X-Forward-To"] = url
        new_headers["Host"] = Url(
            scheme=override.scheme, host=override.host, port=override.port
        ).url
        for header, value in LUMOS_PROXY_HEADERS.items():
            new_headers[header] = value

        # Get request body if applicable
        if request.method in ("POST", "PUT", "PATCH"):
            content = request.content or bytes([])
        else:
            content = None

        new_request = httpx.Request(
            method=request.method,
            url=updated.url,
            headers=new_headers,
            content=content,
        )

        return super(AsyncClient, self).send(new_request, **kwargs)
