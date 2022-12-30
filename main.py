import json
from typing import Final
from gphotospy import authorize
from gphotospy.album import *
from gphotospy.media import Media
import asyncio
import aiohttp
import aiofiles
from Upload_photos import upload_photo

CLIENT_SECRET_FILE = "creds.json"
service = authorize.init(CLIENT_SECRET_FILE)

ALBUM_ID: Final[
    str
] = "AFmVu-sHlfu-jY4R2Kv0wXSQeI_xguLOKgnnUBHVlfgR3J_ceIhtoj3F0Pj-sFGs1inAQNnmKUAL"  # google photos album that you want to download from, get via album_manager.list()
album_manager = Album(service)
media_manager = Media(service)
print("Getting photos...")
album_media_list = list(media_manager.search_album(ALBUM_ID))
photos = []
for k in album_media_list:
    try:
        if k["mimeType"] in ["image/heif"]:
            continue
        elif k["mediaMetadata"]["photo"]["cameraMake"] != "Google":
            continue
    except KeyError:
        pass
    k.pop("productUrl", None)
    k.pop("id", None)
    photos.append(k)

with open("photos.json", "w+") as outfile:
    json.dump(photos, outfile, indent=4)


async def download_photo(photo):  # deprecated, used to download photos to local machine
    url = photo["baseUrl"]
    filename = photo["filename"]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"photos/{filename}", mode="wb")
                await f.write(await resp.read())
                await f.close()


async def create_src_file(photos):
    src = []
    for photo in photos:
        img = await upload_photo(photo["baseUrl"])
        src.append(
            {
                "src": img["image"]["url"],
                "width": img["image"]["width"],
                "height": img["image"]["height"],
                "category": "dog",
            }
        )
    with open("src.json", "w+") as srcfile:
        json.dump(src, srcfile, indent=4)


async def main():
    await create_src_file(photos)
    # await asyncio.gather(*[download_photo(photo) for photo in photos])


asyncio.run(main())


def get_photo_urls():
    items = ""
    for photo in photos:
        items += photo["baseUrl"] + "\n"
    with open("photos.txt", "w+") as outfile:
        outfile.write(items)
