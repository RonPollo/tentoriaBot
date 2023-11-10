from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from workTable import Table
from copy import deepcopy
import json
from datetime import datetime
from text import get_report
import dotenv


from states import Car, Admin


TOKEN = "5938228666:AAFge70Oj-GaBhFMQnPzyu3nzQ1y6McHXeQ"
GOOGLE_CREDENTIALS_FILE = 'tablesApi.json'
# ADMIN_ID=1358843066
ADMIN_ID=439430606
ADMIN_ID1=1


bot = Bot(token=TOKEN)
storage = MemoryStorage() 
dp = Dispatcher(bot=bot, storage=storage)



@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name

    with open('text.txt', 'a') as f:
        f.write(f"{user_id}\t{user_name}\t@{message.from_user.username}\n")
    
    f = open ('names.json', "r")
    data = json.loads(f.read())
    f.close()

    id = data.get(str(message.chat.id), None)



    if message.from_user.id == ADMIN_ID or message.from_user.id == ADMIN_ID1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton(text="Создать новую таблицу")
        item2 = types.KeyboardButton(text="Ссылка на таблицу")
        
        markup.add(item1)
        markup.add(item2)

        await bot.send_message(message.chat.id, "Добро пожаловать администратор", reply_markup=markup)
        await Admin.admin.set()
        return 

    if id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        report = types.KeyboardButton(text="Отчет")
        markup.add(report)

        async with state.proxy() as data:
            data['sheet_name'] = id

        await Car.report.set() # change to car.report
        await message.reply(f"💼Привет, {user_full_name}!", reply_markup=markup)
    else:
        await Car.surname.set()
        await message.reply(f"💼Привет, {user_full_name}!, введите свою Фамилию")


@dp.message_handler(state=Admin.admin)
async def admin_message_handler(message, state: FSMContext):
    if message.text ==  "Создать новую таблицу":
        create_new_table()
        await bot.send_message(message.chat.id, "Таблица успешно создана")
    elif message.text == "Ссылка на таблицу":
        f = open ('names.json', "r")
        data = json.loads(f.read())
        f.close()
        spreadsheetUrl = data.get('spreadsheetUrl', None)
        
        await bot.send_message(message.chat.id, f"Текущая ссылка на таблицу{spreadsheetUrl}")
    else: 
        await bot.send_message(message.chat.id, "Выберите опцию ")

    


def create_new_table():
    tb = Table(GOOGLE_CREDENTIALS_FILE)
    time = datetime.now()
    tb.ss.create(f"{time.year}/{time.month}", f"{time.day}")
    tb.ss.shareWithAnybodyForWriting()
    tb.ss.sheetId
    tb.create_struct_for_sheet()
    with open('names.json', 'r+') as f:
        data = json.load(f)
        data['spreadsheetUrl'] = tb.ss.getSheetURL()
        data['id'] = tb.ss.sheetId
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    del tb


@dp.message_handler(state=Car.surname)
async def handle(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    report = types.KeyboardButton(text="Отчет")
    markup.add(report)


    async with state.proxy() as data:
        data['sheet_name'] = message.text

    with open('names.json', 'r+') as f:
            data = json.load(f)
            data[message.chat.id] = message.text
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    await Car.report.set()
    await bot.send_message(message.chat.id, "Нажмите на кнопку отчет", reply_markup=markup)


@dp.message_handler(state=Car.report)
async def handle(message, state: FSMContext):

    if message.text.lower() == "отчет":
        await Car.number.set()
        await bot.send_message(message.chat.id, "Укажите номер вашей машины")
    else:
        #state = 3
        pass



@dp.message_handler(state=Car.number)
async def handle(message, state: FSMContext):

    try: 
        int(message.text)

        async with state.proxy() as data:
            data['number_car'] = int(message.text)

        await Car.date.set()
        await bot.send_message(message.chat.id, "Укажите дату в формате дд.мм.гг")
    except:
        await bot.send_message(message.chat.id, "Это не номер")


@dp.message_handler(state=Car.date)
async def handle(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    day = types.KeyboardButton(text="🌞День")
    night = types.KeyboardButton(text="🌚Ночь")
    markup.add(day, night)

    try:
        date_list = message.text.split(".")
        if len(date_list) == 3:

 
            for num in date_list:

                if len(num) != 2:
                    raise Exception()
                else:
                    async with state.proxy() as data:
                        data['date'] = message.text

            await Car.period.set()
            await bot.send_message(message.chat.id, "Выберите тип смены", reply_markup=markup)
        else:
            raise Exception()
    except:
        await bot.send_message(message.chat.id, "Формат даты не верен. Повторите попытку")
        


@dp.message_handler(state=Car.period)
async def handler(message, state: FSMContext):
    if message.text == "🌞День":

        async with state.proxy() as data:
            data['period'] = "День"

        await Car.first_distance.set()
        await bot.send_message(message.chat.id, "Введите пробег на начало смены")
        
    elif message.text == "🌚Ночь":
        
        async with state.proxy() as data:
            data['period'] = "Ночь"
        
        await Car.first_distance.set()
        await bot.send_message(message.chat.id, "Введите пробег на начало смены")
    else:
        await bot.send_message(message.chat.id, "Ошибка. Повторите")


@dp.message_handler(state=Car.first_distance)
async def handler(message, state: FSMContext):
    try: 
        num = int(message.text)
        
        async with state.proxy() as data:
            data['first_distance'] = num
        
        await Car.last_distance.set()
        await bot.send_message(message.chat.id, "Введите пробег на конец смены")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")
    

@dp.message_handler(state=Car.last_distance)
async def handler(message, state: FSMContext):
    try: 
        num = int(message.text)
        
        async with state.proxy() as data:
            first_dis = data['first_distance']
            data['last_distance'] = num

        text = f"""Ваш пробег: {num - first_dis}.Введите Z-отчет"""
        await Car.z_report.set()
        await bot.send_message(message.chat.id, text)
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")


@dp.message_handler(state=Car.z_report)
async def handler(message, state: FSMContext):
    

    try:
        z_index = float(message.text)
        
        async with state.proxy() as data:
            data['z_index'] = z_index

        async with state.proxy() as data:
            data['cash_bavaria'] = 0        

        await Car.only_cash.set()
        await bot.send_message(message.chat.id, "Введите наличные баварии")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод") 
        

@dp.message_handler(state=Car.only_cash)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text="Стоп")
    markup.add(stop_item)

    try:
        if message.text != 'Стоп':
             cash = float(message.text)

             async with state.proxy() as data:
                data['cash_bavaria']  =  round(data['cash_bavaria']+cash, 2)
                result = data['cash_bavaria']

             await bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=markup)
        else:
            async with state.proxy() as data:
                data['terminal'] = 0

            await Car.terminal.set()
            await bot.send_message(message.chat.id, "Введите данные терминала")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод") 


@dp.message_handler(state=Car.terminal)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text="Стоп")
    markup.add(stop_item)


    try:
        if message.text != "Стоп":
            terminal = float(message.text)
            
            async with state.proxy() as data:
                data['terminal'] = round(data['terminal']+terminal, 2)
                result = data['terminal'] 

            await bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=markup)
        else:

            async with state.proxy() as data:
                data['viza_discount'] = 0

            await Car.viza_discount.set()
            await bot.send_message(message.chat.id, "Введите visa скидка")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод") 


@dp.message_handler(state=Car.viza_discount)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text="Стоп")
    markup.add(stop_item)

    try: 
        if message.text != "Стоп":
            num = float(message.text)

            async with state.proxy() as data:
                data['viza_discount'] = round(data['viza_discount']+num, 2)
                result = data['viza_discount']

            await bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=markup)
        else:
            async with state.proxy() as data:
                data['cash_card'] = 0
            await Car.cash_card.set()
            await bot.send_message(message.chat.id, "Введите сумму оплат по привязанной карте")

        
    except:
        await bot.send_message(message.chat.id, "Ошибка.Повторите ввод.")


@dp.message_handler(state=Car.cash_card)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text='Стоп')
    markup.add(stop_item)
    try:
        if message.text != "Стоп":
            num = float(message.text)
            
            async with state.proxy() as data:
                data['cash_card'] = round(data['cash_card']+num, 2)
                result = data['cash_card']
            
            await bot.send_message(message.chat.id, f"Результат {result}", reply_markup=markup)
                
        else:

            async with state.proxy() as data:
                data['znf'] = 0
            await Car.znf.set()
            await bot.send_message(message.chat.id, "Введите данные ЗНФ")
    
    
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите вод") 


@dp.message_handler(state=Car.znf)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text='Стоп')
    markup.add(stop_item)

    try:
        if message.text != "Стоп":
            num = float(message.text)

            async with state.proxy() as data:
                data['znf'] = round(data['znf']+num, 2)
                result = data['znf']

            await bot.send_message(message.chat.id, f"Результат {result}", reply_markup=markup)    
         
        else:
            
            async with state.proxy() as data:
                data['perscash'] = 0

            
            await bot.send_message(message.chat.id, "Введите данные по Личному счету")
            await Car.perscash.set()
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод") 


@dp.message_handler(state=Car.perscash)
async def handler(message, state:FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text='Стоп')
    markup.add(stop_item)
    try:
        if message.text !="Стоп":
            num = float(message.text)

            async with state.proxy() as data:
                data['perscash'] = round(data['perscash']+num, 2)
                result = data['perscash']

            await bot.send_message(message.chat.id, f"Результат {result}", reply_markup=markup) 

        else:

            async with state.proxy() as data:
                data['bonuse'] = 0
            await Car.bonuse.set()
            await bot.send_message(message.chat.id, "Введите данные по бонусам")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")


@dp.message_handler(state=Car.bonuse)
async def handler(message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop_item = types.KeyboardButton(text='Стоп')
    markup.add(stop_item)

    try:
        if message.text != "Стоп":
            num = float(message.text)
        
            async with state.proxy() as data:
                data['bonuse'] = round(data['bonuse']+num, 2)
                result = data['bonuse']

            await bot.send_message(message.chat.id, f"Результат {result}", reply_markup=markup)

        else:

            await Car.yandex_nal.set()
            await bot.send_message(message.chat.id, "Введите данные по расчету наличными Яндекс", reply_markup=types.ReplyKeyboardRemove())
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод") 


@dp.message_handler(state=Car.yandex_nal)
async def handler(message, state: FSMContext):
    try:
        yandex_nal = float(message.text)
        
        async with state.proxy() as data:
            data['yandex_nal'] = yandex_nal

        await Car.yandex_bez.set()
        await bot.send_message(message.chat.id, "Введите данные по расчету картой в Яндекс")
    except:
        await bot .send_message(message.chat.id, "Ошибка. Повторите ввод") 


@dp.message_handler(state=Car.yandex_bez)
async def handler(message, state: FSMContext):
    try:
        yandex_bez = float(message.text)

        async with state.proxy() as data:
            data['yandex_bez'] = yandex_bez

        await Car.washing.set()
        await bot.send_message(message.chat.id, "Стоимость мойки, если не мыли авто впишите 0")
    except:
        
        await bot.send_message(message.chat.id, "Ошибка. Повторите попытку")
                

@dp.message_handler(state=Car.washing)
async def handler(message, state: FSMContext):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    washing_nal = types.KeyboardButton(text="Наличные💵")
    washing_bez = types.KeyboardButton(text="Безнал💳")
    markup1.add(washing_nal, washing_bez)
    try:
        washing = float(message.text)

        async with state.proxy() as data:
            data['washing'] = washing

        await Car.type_pay_washing.set()   
        await bot.send_message(message.chat.id, "Выберите способ оплаты мойки", reply_markup=markup1)
    except Exception as e:
        print(f"error: {e}")
        await bot.send_message(message.chat.id, "Ошибка. Повторите выбор")


@dp.message_handler(state=Car.type_pay_washing)
async def handler(message, state: FSMContext):
    try:
        if message.text == 'Наличные💵':

            async with state.proxy() as data:
                data['washing_type'] = 'Наличные'

            await Car.azs.set()
        elif message.text == 'Безнал💳':

            async with state.proxy() as data:
                data['washing_type'] = 'Безнал'

            await Car.azs.set()
        else:
            raise Exception
        
        await bot.send_message(message.chat.id, "Стоимость заправки, если не заправляли авто впишите 0")
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите попытку")



@dp.message_handler(state=Car.azs)
async def handler(message, state: FSMContext): 
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    azs_nal = types.KeyboardButton(text="Наличные💵")
    azs_bez = types.KeyboardButton(text="Безнал💳")
    markup1.add(azs_nal, azs_bez)
    try:
        azs = float(message.text)

        async with state.proxy() as data:
            data['azs'] = azs

        await Car.type_pay_azs.set()
        await bot.send_message(message.chat.id, "Выберите способ оплаты заправки", reply_markup=markup1)
    except:
        print(f"error: {azs}")
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")
        

@dp.message_handler(state=Car.type_pay_azs)
async def handler(message, state: FSMContext):
    try:
        if message.text == 'Наличные💵' or message.text == 'Безнал💳':

            if message.text == 'Наличные💵':

                async with state.proxy() as data:
                    data['azs_type'] = 'Наличные'
                await Car.water.set()
            elif message.text == 'Безнал💳':

                async with state.proxy() as data:
                    data['azs_type'] = 'Безнал'
                await Car.water.set()
            else:
                raise Exception
            
            await bot.send_message(message.chat.id, 'Введите оставшееся количество воды')
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите выбор")
          

@dp.message_handler(state=Car.water)
async def handler(message, state):
    try:
        count = int(message.text)

        async with state.proxy() as data:
                data['water'] = count

        await bot.send_message(message.chat.id, 'Введите количество посадок яндекс')
        await Car.count_yandex.set()
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")


@dp.message_handler(state=Car.count_yandex)
async def handler(message, state):
    try:
        count = int(message.text)

        async with state.proxy() as data:
                data['count_yandex'] = count

        await bot.send_message(message.chat.id, 'Введите количество посадок баварии')
        await Car.count_bavaria.set()
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")


@dp.message_handler(state=Car.count_bavaria)
async def handler(message, state):
    try:
        count = int(message.text)

        async with state.proxy() as data:
                data['count_bavaria'] = count

        await bot.send_message(message.chat.id, 'Количество сданной налички')
        await Car.over_cash.set()
    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите ввод")


@dp.message_handler(state=Car.over_cash)
async def handler(message, state):
    try:
        count = float(message.text)

        async with state.proxy() as data:
                data['over_cash'] = count

                cdata = deepcopy(data._data)
        

        f = open ('names.json', "r")
        data = json.loads(f.read())
        f.close()

        tb = Table(GOOGLE_CREDENTIALS_FILE,  data.get("id"))
        
        if not tb.is_have_list(cdata['sheet_name']):
            tb.create_sheets(cdata['sheet_name'])
            tb.create_struct_for_sheet()

        tb.ss.setSheetByName(cdata['sheet_name'])
        tb.add_items(cdata)  
        
        tb.run()
        report = await get_report(state)
        
        await bot.send_message(message.chat.id, text=report)

    except:
        await bot.send_message(message.chat.id, "Ошибка. Повторите позже.")


if __name__ == '__main__':
    try:
        executor.start_polling(dp)
    except Exception as e:
        with open('errors.txt', 'a') as f: # check in db if username exist
            f.write(e)

 