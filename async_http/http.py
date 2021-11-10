from aiohttp import ClientSession
from json import dumps


async def post(url, data, headers=None):
    async with ClientSession() as s:
        if headers:
            async with s.post(url=url, headers=headers, data=data) as response:
                result = await response.json()
                return result
        else:
            async with s.post(url=url, data=data) as response:
                result = await response.json()
                return result
