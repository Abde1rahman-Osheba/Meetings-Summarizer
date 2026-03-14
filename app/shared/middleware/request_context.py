from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):  # type: ignore[override]
        request.state.request_id = request.headers.get("x-request-id", "generated-request-id")
        return await call_next(request)
