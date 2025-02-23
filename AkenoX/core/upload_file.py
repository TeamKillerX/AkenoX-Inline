import aiofiles
import aiohttp


async def upload_to_catbox(dl_path: str) -> str:
    base_url = "https://catbox.moe/user/api.php"

    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field("reqtype", "fileupload")

        async with aiofiles.open(dl_path, mode="rb") as file:
            file_data = await file.read()
            form_data.add_field(
                "fileToUpload",
                file_data,
                filename=dl_path.split("/")[-1],
                content_type="application/octet-stream"
            )

        async with session.post(base_url, data=form_data) as response:
            response.raise_for_status()
            return (await response.text()).strip()
