from .. import loader, utils
import aiohttp
import io
import base64

API_KEY = "sk-UD33pBtFhZQB46zVTJ2YMbicViPSMU4wT9gscHzb3hwzXCZT"
API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"

@loader.tds
class SimpleAiImageGen(loader.Module):
    """Генерация изображений через Stable Diffusion API"""

    strings = {
        "name": "SimpleAiImageGen",
        "no_prompt": "⚠️ Укажи описание для генерации изображения.",
        "generating": "⏳ Генерирую изображение...",
        "error": "❌ Ошибка при генерации изображения.",
    }

    async def _generate_image(self, prompt, message):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

        json_data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30
        }

        await message.edit(self.strings["generating"])

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(API_URL, headers=headers, json=json_data) as resp:
                    resp.raise_for_status()
                    data = await resp.json()

            img_b64 = data["artifacts"][0]["base64"]
            img_bytes = base64.b64decode(img_b64)

            with io.BytesIO(img_bytes) as img_file:
                img_file.name = "result.png"
                await message.client.send_file(message.chat_id, img_file, reply_to=message.id)

            await message.delete()

        except Exception as e:
            await message.edit(f"{self.strings['error']} ({e})")

    async def genphoto_cmd(self, message):
        """Команда .genphoto <описание> — генерация картинки по описанию"""
        prompt = utils.get_args_raw(message)
        if not prompt:
            await message.edit(self.strings["no_prompt"])
            return
        await self._generate_image(prompt, message)

    async def genphoto_kot_cmd(self, message):
        """Команда .genphoto_kot <описание> — пример с подчёркиванием"""
        prompt = utils.get_args_raw(message)
        if not prompt:
            await message.edit(self.strings["no_prompt"])
            return
        await self._generate_image(prompt, message)
