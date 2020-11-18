# ---------------------------------------------- #
# Plugin Name           : BitmexLiquidationFeed  #
# Author Name           : vsnz                   #
# File Name             : main.py                #
# ---------------------------------------------- #

import config

from telegram import Bot
from discord_webhook import DiscordWebhook
import logging
import asyncio as aio
import websockets
import json

loop = aio.get_event_loop()

async def receive_data():
    ws = await websockets.connect("wss://www.bitmex.com/realtime?subscribe=liquidation:XBTUSD,liquidation:ETHUSD")
    while True:
        try:
            if not ws.open:
                print ('Reconnecting...')
                ws = await websockets.connect("wss://www.bitmex.com/realtime?subscribe=liquidation:XBTUSD,liquidation:ETHUSD")
            try:
                data = await aio.wait_for(ws.recv(), timeout=20)
            except aio.TimeoutError:
                try:
                    pong_waiter = await ws.ping()
                    await aio.wait_for(pong_waiter, timeout=10)
                except aio.TimeoutError:
                    break
            except Exception as e:  
                print(e)
            else:
                print('.', end='', flush=True)
                await handle_feed(data)
        except BaseException:
                time.sleep(5)
    print('Client closed')
    ws.close()

async def handle_feed(data):
    x = json.loads(data)
    if 'table' in x and x['table'] == 'liquidation':
        if 'action' in x and x['action'] == 'insert':
            if 'data' in x and isinstance(x['data'], list):
                if float(x['data'][0]['leavesQty']) > config.liquidation_threshold:

                    side        = 'SHORT' if x['data'][0]['side'] == 'Buy' else 'LONG'
                    contracts   = '{:,.0f}'.format(float(x['data'][0]['leavesQty']))
                    price       = '{:,.2f}'.format(float(x['data'][0]['price']))
                    ticker      = x['data'][0]['symbol']

                    liquidation = f'Liquidated #{side} ${ticker} {contracts} contracts at ${price}!'

                    if config.send_terminal_alerts:
                        print(liquidation)

                    if config.telegram:
                        tg_bot = Bot(token=config.tg_token)
                        tg_bot.sendMessage(config.channel, liquidation)

                    if config.discord:
                        discord_alert = DiscordWebhook(url=config.discord_webhook, content=liquidation)
                        response = discord_alert.execute()

if __name__ == '__main__':
    try:
        print("Bot started. Looking for new liquidations on Bitmex. . .")
        loop.run_until_complete(receive_data())
        loop.close()
    except KeyboardInterrupt:
        print('Interrupted')