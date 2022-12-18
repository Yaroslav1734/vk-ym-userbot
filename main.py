import asyncio
from config import *
from vkbottle import User
from vkbottle.user import Message
from vkbottle.dispatch.rules.base import CommandRule
from yandex_music import ClientAsync
import random


vk = User(VK_TOKEN)
ym = ClientAsync(YANDEX_MUSIC_TOKEN)


async def main():
    await ym.init()
    await vk.api.messages.send(
        random_id=random.randint(1000, 999999),
        message=f"Юзербот активен. Для помощи напишите {PREFIX}help",
    )


async def get_track_info():
    queues = await ym.queues_list()
    last_queue = await ym.queue(queues[0].id)
    track_id = last_queue.get_current_track()
    track = await track_id.fetch_track_async()
    artists = ", ".join(track.artists_name())
    title = track.title
    return f"{artists} - {title}"


@vk.on.message(CommandRule("help", [PREFIX]))
async def help(message: Message):
    await message.ctx_api.messages.edit(
        message.peer_id,
        f"""
    Команды:
        {PREFIX}help - Получить список команд
        {PREFIX}now - Получить трек, который играет сейчас в яндекс музыке
    """,
        message_id=message.id,
    )


@vk.on.message(CommandRule("now", [PREFIX]))
async def now(message: Message):
    await message.ctx_api.messages.edit(
        message.peer_id, await get_track_info(), message_id=message.id
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    coro1 = vk.run_polling()
    coro2 = main()
    loop.run_until_complete(coro1)
    loop.run_until_complete(coro2)
