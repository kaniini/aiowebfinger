import asyncio
import aiohttp
import aiohttp.client_exceptions
import xml.etree.ElementTree as etree

from aiowebfinger import __version__
from aiowebfinger.errors import WebFingerException
from aiowebfinger.response import JRDResponse, XRDResponse


class HTTPClientError(WebFingerException):
    pass


class MalformedResourceError(WebFingerException):
    pass


class WebFingerClient:
    def __init__(self, rewrite_endpoints_map: dict={}):
        self.rewrite_endpoints_map = rewrite_endpoints_map

    async def finger(self, resource: str, host: str=None, rel: str=None, raw: str=None):
        if not host:
            host = resource.split('@')[-1]

        if not host:
            raise MalformedResourceError('Resource %r is malformed' % resource)

        # if host endpoint is to be rewritten, use the rewrite, otherwise use the original input
        host = self.rewrite_endpoints_map.get(host, host)

        headers = {
            'User-Agent': 'aiowebfinger/%s' % __version__,
            'Accept': 'application/jrd+json, application/json, application/xml'
        }

        uri = 'https://%s/.well-known/webfinger' % host

        params = {'resource': resource}
        if rel:
            params['rel'] = rel

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(uri, headers=headers, params=params) as resp:
                    if resp.status != 200:
                        return

                    ctype = resp.headers.get('Content-Type', 'application/xml')
                    if 'application/xml' in ctype:
                        et = etree.XML((await resp.text()))
                        return XRDResponse(et)

                    return JRDResponse((await resp.json(content_type=ctype)))
        except aiohttp.client_exceptions.ClientError as exc:
            raise HTTPClientError(exc)
