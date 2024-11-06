import sys
import threading
from dataclasses import dataclass

import pytest
from connector.httpx_rewrite import AsyncClient, add_proxy_headers, set_proxy_host
from flask import Flask, request


@dataclass
class RecordedRequest:
    method: str
    path: str
    headers: dict[str, str]
    body: str | None = None


class Recorder:
    request: RecordedRequest | None = None

    def get_request(self) -> RecordedRequest:
        assert self.request is not None
        return self.request

    def proxy_request(self) -> str:
        self.request = RecordedRequest(
            headers={key: val for key, val in request.headers.items()},
            path=request.path,
            method=request.method,
        )
        return "Dummy response body"

    def reset_request(self) -> None:
        """
        This is necessary because
        1. the server calling this recorder is only created once
            (to avoid port conflicts from rapid server shutdown/recreation)
        2. so this recorder is only created once, and is thus a global test object :(
        """
        self.request = None


@pytest.fixture(scope="session")
def port() -> int:
    return 4444


@pytest.fixture(scope="session")
def recorder(port):
    # Turn off Flask's default logging
    sys.modules["flask.cli"].show_server_banner = lambda *x: None  # type: ignore

    recorder = Recorder()
    app = Flask(__name__)
    app.route("/proxy")(recorder.proxy_request)
    thread = threading.Thread(target=app.run, daemon=True, kwargs=dict(host="localhost", port=port))
    thread.start()
    yield recorder


@pytest.fixture
def client(recorder: Recorder, port: int) -> AsyncClient:
    recorder.reset_request()
    set_proxy_host(f"http://localhost:{port}")
    return AsyncClient()


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_forwarding_happens(self, recorder: Recorder, client: AsyncClient) -> None:
        """We should call our running server instead of the original host"""
        await client.get("https://hope-nobody-ever-registers-this-domain.com/hi")
        assert recorder.request is not None
        assert recorder.request.method == "GET"
        assert recorder.request.path == "/proxy"

    @pytest.mark.asyncio
    async def test_forward_to_header_is_added(
        self, recorder: Recorder, client: AsyncClient
    ) -> None:
        """The receiving proxy should get called with an X-Forward-To header with the original request line"""
        await client.get("https://hope-nobody-ever-registers-this-domain.com/hi")

        proxy_received_request = recorder.get_request()
        assert (
            proxy_received_request.headers["X-Forward-To"]
            == "https://hope-nobody-ever-registers-this-domain.com/hi"
        )

    @pytest.mark.asyncio
    async def test_proxy_headers_are_sent(self, recorder: Recorder, client: AsyncClient) -> None:
        """The receiving proxy should get called with other headers included in the request"""
        add_proxy_headers({"Absolutely-Fake": "yep this is here"})
        await client.get("https://hope-nobody-ever-registers-this-domain.com/hi/there")
        proxy_received_request = recorder.get_request()
        assert proxy_received_request.headers["Absolutely-Fake"] == "yep this is here"

    @pytest.mark.asyncio
    async def test_other_headers_are_sent(self, recorder: Recorder, client: AsyncClient) -> None:
        """The receiving proxy should get called with other headers included in the request"""
        await client.get(
            "https://hope-nobody-ever-registers-this-domain.com/hi/there",
            headers={
                "Foo": "Bar",
                "Authorization": "Bearer SUPER_SECRET",
            },
        )
        proxy_received_request = recorder.get_request()
        assert proxy_received_request.headers["Foo"] == "Bar"
        assert proxy_received_request.headers["Authorization"] == "Bearer SUPER_SECRET"

    @pytest.mark.asyncio
    async def test_no_proxy_host_means_no_proxy_calls(
        self, recorder: Recorder, client: AsyncClient
    ) -> None:
        """If there's no proxy host set, call the actual domain"""
        set_proxy_host(None)
        response = await client.get(
            "https://www.google.com"  # I assume this will be around for most tests
        )
        assert response.request.url == "https://www.google.com"
        assert response.status_code == 200
        assert recorder.request is None
