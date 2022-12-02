from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
import requests
import base64 
import json
import os

bot = Bot(token="") #Тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Не флуди, я тебя с первого раза понял!")
    
@dp.message_handler(commands="start")
@dp.throttled(anti_flood,rate=1)
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Добро пожаловать в бота T.I.A.T\nРасшифровываемся мы как: turning into a tian\nЯ обработаю ваше фото в аниме с помощью китайской нейронки\n\nМожешь просто отправить фото, и я начну обработку")
    pass
    
@dp.message_handler(content_types=["photo"])
@dp.throttled(anti_flood,rate=0.5)
async def get_photo(message):
    chat_id = message.chat.id
    msg = await bot.send_message(chat_id, "Начинаю обработку...")
    try:
        await message.photo[-1].download(f'photo/{chat_id}.png')
        image = open(f'photo/{chat_id}.png', 'rb')
        image_read = image.read()
        encoded_string = base64.b64encode(image_read)
    
        data = {
        "busiId": "ai_painting_anime_img_entry",
        "images": [f"{encoded_string.decode('utf-8')}"],
        "extra": "{\"face_rects\":[],\"version\":2,\"platform\":\"web\",\"data_report\":{\"parent_trace_id\":\"bfd12fae-1c76-0c8c-b60f-6ca82cb842e7\",\"root_channel\":\"qq_sousuo\",\"level\":11}}"}
    
        await msg.edit_text("Отправляю запрос сервису на обработку...")
    
        result = requests.post('https://ai.tu.qq.com/trpc.shadow_cv.ai_processor_cgi.AIProcessorCgi/Process', json=data)
        await msg.edit_text("Расшифровываем ответ...")
        respons = json.loads(result.text)
        search = json.loads(respons['extra'])
        site = search["img_urls"][0]
        await msg.delete()
        await bot.send_photo(chat_id, photo=f'{site}', caption=f'💎Ля как красиво получилось!\nПорекомендуй мой сервис друзьям, тебе не сложно а мне приятно\nРазработчик: @CTOHKC', parse_mode='html')
    except:
        await msg.edit_text("Сервер прислал ошибку.\nСкорее всего сеть просто перегружена\nПопробуйте через 2-3 минутки снова\nУ вас получится, я обещаю)")
    os.remove(f'photo/{chat_id}.png')
    pass
    
while True:
    try:
        if __name__ == "__main__":
            executor.start_polling(dp, skip_updates=True)
        break
    except:
        print("Ошика.\nОжидаем перезапуск 20 сек...")
        time.sleep(20)