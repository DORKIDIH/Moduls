from .. import loader, utils
import requests

@loader.tds
class ImgGenMod(loader.Module):
    """Генерация изображений через нейросеть по prompt"""

    strings = {
        "name": "ImgGen",
        "no_prompt": "⚠️ Укажи текст для генерации изображения.",
        "generating": "⏳ Генерирую изображение...",
        "error": "❌ Ошибка при генерации изображения.",
    }

    async def imgcmd(self, message):
        """Использование: .img <текст> - генерация изображения по тексту"""
        prompt = utils.get_args_raw(message)
        if not prompt:
            await message.edit(self.strings("no_prompt"))
            return

        await message.edit(self.strings("generating"))

        # Пример для stablediffusionapi.com (замени YOUR_API_KEY на реальный)
        API_KEY = "YOUR_API_KEY"
        url = "https://stablediffusionapi.com/api/v3/text2img"
        params = {
            "key": API_KEY,
            "prompt": prompt,
            "negative_prompt": "",
            "width": "512",
            "height": "512",
            "samples": "1",
            "num_inference_steps": "30",
            "seed": None,
            "guidance_scale": 7.5,
            "webhook": None,
            "track_id": None
        }

        try:
            resp = requests.post(url, json=params)
            data = resp.json()
            if data.get("status") != "success":
                await message.edit(self.strings("error"))
                return
            image_url = data["output"][0]
            await message.client.send_file(message.chat_id, image_url, reply_to=message.id)
            await message.delete()
        except Exception as e:
            await message.edit(self.strings("error"))
