from .. import loader, utils
import requests

@loader.tds
class MemeGenMod(loader.Module):
    """Генератор мемов через imgflip API"""

    strings = {
        "name": "MemeGen",
        "usage": "Использование:\n.imgmeme <шаблон> | <верхний текст> | <нижний текст>\nПример:\n.imgmeme distracted_boyfriend | Когда код работает | Но ты не понимаешь почему",
        "error": "❌ Ошибка при создании мема.",
        "no_args": "⚠️ Укажи шаблон и тексты через |",
    }

    async def imgmemecmd(self, message):
        """Генерирует мем по шаблону"""
        args = utils.get_args_raw(message)
        if not args or '|' not in args:
            await message.edit(self.strings("no_args"))
            return

        parts = [x.strip() for x in args.split('|')]
        if len(parts) < 3:
            await message.edit(self.strings("no_args"))
            return

        template_name, top_text, bottom_text = parts[:3]

        await message.edit("⏳ Создаю мем...")

        templates = {
            "distracted_boyfriend": "112126428",
            "drake": "181913649",
            "two_buttons": "87743020",
            "gru_plan": "131087935",
            "change_my_mind": "129242436",
        }

        template_id = templates.get(template_name.lower())
        if not template_id:
            await message.edit("⚠️ Шаблон не найден. Доступные шаблоны:\n" + ", ".join(templates.keys()))
            return

        USERNAME = "Hlensossal1"
        PASSWORD = "19912806"

        payload = {
            'template_id': template_id,
            'username': USERNAME,
            'password': PASSWORD,
            'text0': top_text,
            'text1': bottom_text
        }

        try:
            resp = requests.post("https://api.imgflip.com/caption_image", data=payload)
            res = resp.json()
            if res['success']:
                url = res['data']['url']
                await message.client.send_file(message.chat_id, url, reply_to=message.id)
                await message.delete()
            else:
                await message.edit(self.strings("error"))
        except Exception as e:
            await message.edit(f"{self.strings('error')} ({e})")
