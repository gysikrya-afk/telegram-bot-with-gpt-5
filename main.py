import asyncio
from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart,StateFilter
from aiogram.fsm.context import FSMContext
from openai import AsyncOpenAI

bot = Bot(token='BOT_TOKEN')
dp = Dispatcher()
client = AsyncOpenAI(api_key='API_KEY')

async def create_responce(text:str):
    responce = await client.responses.create(
        model='gpt-5',
        input = text
    )
    return responce.output_text

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer('Привет.Я тедешрам бот с встроеным ИИ.') 

@dp.message(StateFilter('Generating'))
async def wait_responce(message:Message):
    await message.answer('Идёт генерация ответа...') 

@dp.message()
async def generate_answer(message:Message,state:FSMContext):
    await state.set_state('Generating') 

    try:
        responce = await create_responce(message.text)
    except Exception as e :
        await message.answer(f'Произашла ошибка:{e}.Извените за неполадки.')
    else:
        await message.answer(responce)
    finally:
        await state.clear()

if __name__ == '__main__':
    asyncio.run(main())
