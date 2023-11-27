from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import MessageEntityType

from utils.web_parser_connector import url_parser

from collections import OrderedDict

from text.text import get_text
from utils import serrializer

from database import firebase_db as fb

router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        text=get_text("greeting"),
    )


@router.message(StateFilter(None), Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        text=get_text("more_info"),
    )


@router.message(StateFilter(None), F.entities[:].type == MessageEntityType.URL)
async def url_parse(message: types.Message):
    if len(message.entities) > 1:
        await message.answer(text="Умею обрабатывать только по одной ссылке за раз")
    url = message.entities[0].url

    resp_gift = await url_parser.wait_response()
    content = serrializer.gift_to_str(resp_gift)

    await message.answer(**content.as_kwargs())


class TopCommandState(StatesGroup):
    one_more = State()


async def remove_prev_msg_inline_keyboard(bot, data: dict):
    if "prev_msg" not in data.keys():
        return
    prev_msg = data["prev_msg"]
    await bot.edit_message_reply_markup(**prev_msg)


async def one_more_gift(message: types.Message, state: FSMContext):
    batch_size = 10
    data = await state.get_data()

    await remove_prev_msg_inline_keyboard(message.bot, data)

    cache: OrderedDict = data.get("cached_response", None)
    first_call = False
    if not cache:
        ref = fb.db.reference("/gift_list/").order_by_child("score")
        prev_batch_start_score = data.get("last_score", None)
        if prev_batch_start_score:
            ref = ref.end_at(prev_batch_start_score)
        else:
            first_call = True
        limited_ref = ref.limit_to_last(batch_size)
        cache = await fb.q_get(limited_ref)
        data["cached_response"] = cache
        if cache and not first_call:
            cache.popitem(last=True)
        if not cache:
            text = "Это все варианты, что я нашел"
            if first_call:
                text = "Не смог найти подходящих вариантов 😭"
            await state.clear()
            print("Cleared")
            await message.answer(text=text)
            return
        data["last_score"] = next(iter(cache.values()))["score"]

    to_send = cache.popitem(last=True)[1]
    content = serrializer.gift_to_str(to_send)

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="ещё", callback_data="top_more"),
        types.InlineKeyboardButton(text="стоп", callback_data="top_finish")
    )

    msg: types.Message = await message.answer(**content.as_kwargs(),
                                              reply_markup=builder.as_markup(),
                                              disable_notification=True)

    data["prev_msg"] = {"chat_id": msg.chat.id, "message_id": msg.message_id}
    print("data")
    print(data)
    await state.set_data(data)


@router.message(StateFilter(None), Command("top"))
async def cmd_top(message: types.Message, state: FSMContext):
    await state.set_state(TopCommandState.one_more)
    await one_more_gift(message, state)


@router.callback_query(TopCommandState.one_more, F.data == "top_more")
async def top_more(callback: types.CallbackQuery, state: FSMContext):
    await one_more_gift(callback.message, state)
    await callback.answer()


@router.callback_query(TopCommandState.one_more, F.data == "top_finish")
async def top_finish(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await remove_prev_msg_inline_keyboard(callback.bot, data)
    await state.clear()
    await callback.answer(text="Спасибо!")
