from io import BytesIO
import codecs
import html
import os
import random
import re
from random import randint
from typing import Optional
import requests
from requests import get
from wbb import app, eor
from pyrogram import filters
from pyrogram.errors import BadRequest

@app.on_message(filters.command("ud"))
async def ud(bot, message):
    msg = message.text.replace("/ud", "")
    if not msg:
        await eor(message, text="Please enter keywords to search!")
        return
    try:
        results = get(f"http://api.urbandictionary.com/v0/define?term={msg}").json()
        reply_text = f'Word: {msg}\nDefinition: {results["list"][0]["definition"]}'
        reply_text += f'\n\nExample: {results["list"][0]["example"]}'
    except IndexError:
        reply_text = (
            f"Word: {text}\nResults: Sorry could not find any matching results!"
        )
    ignore_chars = "[]"
    reply = reply_text
    for chars in ignore_chars:
        reply = reply.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]  # max msg lenth of tg.
    try:
        await eor(message, text=reply)
    except BadRequest as err:
        await eor(message, text=f"Error! \n \n {err.message}")