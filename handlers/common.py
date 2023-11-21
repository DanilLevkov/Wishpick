from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from text.text import get_text

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text=get_text("greeting"),
    )


@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(
        text=get_text("more_info"),
    )
