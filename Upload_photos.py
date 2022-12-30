import aiohttp


async def upload_photo(url):
    form_data = aiohttp.FormData()
    # Add fields to the FormData object
    form_data.add_field('source', url)
    form_data.add_field('type', 'url')
    form_data.add_field('action', 'upload')
    async with aiohttp.ClientSession() as session:
        async with session.post('https://freeimage.host/json', data=form_data) as response:
            return await response.json()


