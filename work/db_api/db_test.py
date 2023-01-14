from work.db_api.db_bot_user import *
from work.config import *
from work.db_api import quick_commands
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yfinance as yf
import aioschedule
import asyncio

data_check = []

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


async def db_test():
        await db.set_bind(postgres_url)
        await db.gino.create_all()

        tickers = ['PM']
        for ticker in tickers:
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            data1_close = data['Close'].iloc[-1]
            data1_open = data['Open'].iloc[-1]
            data1_low = data['Low'].iloc[-1]
            data1_high = data['High'].iloc[-1]
            if data1_open > 0 and data1_close > 0 and data1_low > 0 and data1_high > 0:
                data_check.extend((data1_open, data1_close, data1_high, data1_low))
                print(data_check)
                await quick_commands.add_user(1, str(data1_open), 'Open')
                await quick_commands.add_user(2, str(data1_close), 'Close')
                await quick_commands.add_user(3, str(data1_high), 'High')
                await quick_commands.add_user(4, str(data1_low), 'Low')
                await bot.send_message(chat_id=ADMIN_ID, text='Все переменные положительные')

                users = await quick_commands.select_all_users()
                print(users)

                count = await quick_commands.count_users()
                print(count)

                user_open = await quick_commands.select_user(1)
                user_close = await quick_commands.select_user(2)
                user_high = await quick_commands.select_user(3)
                user_low = await quick_commands.select_user(4)

                if str(data1_open) != user_open.name or str(data1_close) != user_close.name\
                        or str(data1_high) != user_high.name or str(data1_low) != user_low.name:
                    await quick_commands.update_user_name(1, str(data1_open))
                    await quick_commands.update_user_name(2, str(data1_close))
                    await quick_commands.update_user_name(3, str(data1_high))
                    await quick_commands.update_user_name(4, str(data1_low))
                    await bot.send_message(chat_id=ADMIN_ID, text='Добавлены новые данные в бд')
                else:
                    await bot.send_message(chat_id=ADMIN_ID, text='Ошибка! \nне обнаружено новых данных в бд')
                    aioschedule.every().hour.do(main())
            else:
                await bot.send_message(chat_id=ADMIN_ID, text='Присутствуют отрицательные переменные')


# await quick_commands.update_user_name(1, 'New Maxim Name_1')
    #
    # user_number = await quick_commands.select_user(1)
    # print(user_number)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(db_test())


async def main():
    aioschedule.every().day.at("9:30").do(db_test)
    # aioschedule.every().minute.do(db_test)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    executor.start_polling(dp, skip_updates=True)
