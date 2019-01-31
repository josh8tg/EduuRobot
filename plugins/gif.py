
# Copyright (C) 2018-2019 Amano Team <contact@amanoteam.ml>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from config import bot, bot_username, keys
import requests
import random


giphy_key = keys['giphy']


def gif(msg):
    if msg.get('text'):
        if msg['text'].startswith('/gif ') or msg['text'].startswith('!gif '):
            text = msg['text'][5:]
            rjson = requests.get(
                "http://api.giphy.com/v1/gifs/search", params=dict(q=text, api_key=giphy_key, limit=7)).json()
            if rjson["data"]:
                res = random.choice(rjson["data"])
                result = res["images"]["original_mp4"]["mp4"]
                bot.sendVideo(msg['chat']['id'], result,
                              reply_to_message_id=msg['message_id'])
            else:
                bot.sendMessage(msg['chat']['id'], "Sem resultados",
                                reply_to_message_id=msg['message_id'])
