import os
import logging
from signalbot import SignalBot, Command, Context, triggered, enable_console_logging

import local_secrets as sc

import images
from PIL import Image
import base64
from io import BytesIO
import epd7in5_V2_old
import time

def img_to_b64(img: Image):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def b64_to_img(b64: str):
    return Image.open(BytesIO(base64.b64decode(b64)))

async def handleMessage(c: Context) -> None:
    if c.message.source_number == sc.SHOW_MESSAGES_FROM_NR:
        img = None
        for attachment in c.message.base64_attachments:
            try:
                img = b64_to_img(attachment)
                break
            except Exception as e:
                pass

        if img:
            img_bnw = images.convert_image(img)
            display_image(img_bnw)
            await c.send(
                "",
                base64_attachments=[img_to_b64(img_bnw)],
            )
            time.sleep(1)
        elif c.message.text:
            img = images.convert_text(c.message.text)
            display_image(img)
            await c.send(
                "",
                base64_attachments=[img_to_b64(img)],
            )
            time.sleep(1)
        else:
            await c.reply("I don't know what to do with that message.")

        await c.react(sc.REACTION_EMOJI)

def display_image(img: Image):
    epd = epd7in5_V2_old.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))

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
