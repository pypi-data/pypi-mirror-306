from ipaddress import ip_address

import httpx
from starlette.datastructures import Headers


async def _do_send(r, send):
    log = None

    await send({
        "type": "http.response.start",
        "status": r.status_code,
        "headers": [(k.encode(), v.encode()) for k, v in r.headers.items()],
    })

    # Stream the content
    try:
        # aiter_raw not aiter_bytes because we don't want
        # content decoding to have been applied
        async for chunk in r.aiter_raw():
            await send({
                "type": "http.response.body",
                "body": chunk,
                "more_body": True,
            })
    except Exception as e:
        # The client has disconnected
        if log:
            log.info(f"Client disconnected: {e.__class__.__name__}: {e}")

    await send({"type": "http.response.body", "more_body": False})


async def script_response(scope, receive, send):
    async with (
        httpx.AsyncClient() as client,
        client.stream("GET", "https://plausible.io/js/script.js", timeout=10) as r,
    ):
        await _do_send(r, send)


def anonymize_ip(ip):
    ip_bytes = bytearray(ip_address(ip).packed)
    if len(ip_bytes) == 4:  # IPv4
        ip_bytes[3] = 0
    elif len(ip_bytes) == 16:  # IPv6
        for i in range(8, 16):
            ip_bytes[i] = 0
    return str(ip_address(bytes(ip_bytes)))


def anonymize_xff(header):
    try:
        ips = (ip.strip() for ip in header.split(","))
        return ",".join(map(anonymize_ip, filter(None, ips)))
    except Exception:
        return ""


async def event_response(scope, receive, send):
    headers = Headers(scope=scope)

    more_body = True
    body = b""
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body")

    async with (
        httpx.AsyncClient() as client,
        client.stream(
            "POST",
            "https://plausible.io/api/event",
            headers={
                "content-type": "application/json",
                "x-forwarded-for": anonymize_xff(headers.get("x-forwarded-for", "")),
                "user-agent": headers.get("user-agent", ""),
            },
            data=body,
            timeout=10,
        ) as r,
    ):
        await _do_send(r, send)


def plausible(application):
    async def middleware(scope, receive, send):
        if scope["type"] != "http":
            await application(scope, receive, send)
            return

        if scope["path"] == "/js/script.js":
            await script_response(scope, receive, send)
        elif scope["path"] == "/api/event":
            await event_response(scope, receive, send)
        else:
            await application(scope, receive, send)

    return middleware
