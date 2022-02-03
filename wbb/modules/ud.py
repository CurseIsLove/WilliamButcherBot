from io import BytesIO
import codecs
import html
import os
import random
import re
from random import randint
from typing import Optional
import requests
import wikipedia
from requests import get
from wbb import app
from pyrogram import filters
from pyrogram.errors import BadRequest

@app.on_message(filters.command("ud"))
def ud(bot, message):
    msg = message.text.replace("/ud", "")
    if not msg:
        message.reply_text("Please enter keywords to search!")
        return
    try:
        results = get(f"http://api.urbandictionary.com/v0/define?term={msg}").json()
        reply_text = f'Word: {text}\nDefinition: {results["list"][0]["definition"]}'
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
        message.reply_text(reply)
    except BadRequest as err:
        message.reply_text(f"Error! {err.message}")