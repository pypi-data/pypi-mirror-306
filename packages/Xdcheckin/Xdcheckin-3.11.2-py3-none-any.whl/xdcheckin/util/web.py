__all__ = ("compress_middleware", )

from aiohttp.hdrs import CACHE_CONTROL as _CACHE_CONTROL
from aiohttp.web import middleware as _middleware
from aiohttp_compress import compress_middleware as _compress_middleware

from aiohttp.web import Request, StaticResource as _StaticResource

@_middleware
async def compress_middleware(req: Request, handler):
	r = req.match_info.route.resource
	if isinstance(r, _StaticResource) and r._prefix == "/static":
		res = await _compress_middleware(req, handler)
		res.headers[_CACHE_CONTROL] = "public, max-age=86400"
		return res
	return await handler(req)
