import os
import logging
from signalbot import SignalBot, Command, Context, triggered, enable_console_logging

import local_secrets as sc


async def handleMessage(c: Context) -> None:
    print("doing stuff with message")
    if c.message.source_number == sc.SHOW_MESSAGES_FROM_NR:
        print(c.message.text)

        await c.react(sc.REACTION_EMOJI)

class PingCommand(Command):

    async def handle(self, c: Context) -> None:
        try:
            await handleMessage(c)
        except Exception as e:
            await c.reply(f"Error: {e}")


if __name__ == "__main__":
    enable_console_logging(logging.WARNING)

    bot = SignalBot({
        "signal_service": "127.0.0.1:8080",
        "phone_number": sc.BOT_PHONE_NUMBER,
    })
    bot.register(PingCommand(), contacts=False, groups=[sc.GROUP_NAME]) # Run the command for all contacts and groups

    logging.info("Starting bot")
    bot.start()