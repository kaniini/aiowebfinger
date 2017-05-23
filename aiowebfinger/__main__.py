import asyncio
import sys

from aiowebfinger.errors import WebFingerException
from aiowebfinger.client import WebFingerClient
from aiowebfinger.response import RELS


loop = asyncio.get_event_loop()


FINGER_RELS = ['subject'] + [k for k in RELS.keys()]


async def finger(client, resource):
    try:
        resp = await client.finger(resource)
    except WebFingerException as exc:
        print('---', '%s:' % resource, repr(exc))
        print()
        return

    print('---', resource, '---')

    [print('%s:' % k, getattr(resp, k)) for k in RELS if getattr(resp, k)]

    print()


def main():
    client = WebFingerClient()

    futures = [finger(client, i) for i in sys.argv[1:]]
    loop.run_until_complete(asyncio.gather(*futures))


if __name__ == '__main__':
    main()
