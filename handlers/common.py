from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from collections import OrderedDict

from text.text import get_text
from utils import parsers
from utils import serrializer

from database import firebase_db as fb

router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text=get_text("greeting"),
    )


@router.message(StateFilter(None), Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        text=get_text("more_info"),
    )


class TopCommandState(StatesGroup):
    one_more = State()


async def one_more_gift(message: Message, state: FSMContext):
    batch_size = 10
    data = await state.get_data()
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
        if not first_call:
            cache.popitem(last=True)
        if not cache:
            text = "Это все варианты, что я нашел"
            if first_call:
                text = "Не смог найти подходящих вариантов 😭"
            await state.clear()
            await message.answer(
                text=text,
                reply_markup=ReplyKeyboardRemove()
            )
            return
        data["last_score"] = next(iter(cache.values()))["score"]

    to_send = cache.popitem(last=True)[1]
    content = serrializer.gift_to_str(to_send)

    keyboard = None
    if first_call:
        kb = [[
            KeyboardButton(text="Ещё"),
            KeyboardButton(text="Стоп")
        ]]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Можете посмотреть ещё варианты"
        )
    await message.answer(**content.as_kwargs(), reply_markup=keyboard)

    await state.set_data(data)
    await state.set_state(TopCommandState.one_more)


@router.message(StateFilter(None), Command("top"))
async def cmd_top(message: Message, state: FSMContext):
    await one_more_gift(message, state)


@router.message(TopCommandState.one_more, F.text.lower() == "ещё")
async def top_more(message: Message, state: FSMContext):
    await one_more_gift(message, state)


@router.message(TopCommandState.one_more, F.text.lower() == "стоп")
async def top_finish(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Спасибо",
        reply_markup=ReplyKeyboardRemove()
    )
