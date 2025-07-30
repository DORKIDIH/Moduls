# meta developer: @DORKIDIH

from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class GaySayMod(loader.Module):
    """Говорит 'я гей'"""

    strings = {"name": "GaySay"}

    @loader.command()
    async def gay(self, message: Message):
        """Пишет 'я гей'"""
        await utils.answer(message, "я гей")
