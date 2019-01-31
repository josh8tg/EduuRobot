
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

from config import bot, bot_username
import requests
import re
import urllib


def treatTitle(title):
    title = title.replace("_", " ")
    title = title.replace("[", "(")
    title = title.replace("]", ")")
    title = title.replace("(", "(")
    title = title.replace(")", ")")
    return title


def reddit(msg):
    if msg.get('text'):
        if msg['text'].startswith('/r ') or msg['text'].startswith('!r '):
            sub = msg['text'][3:]
            if sub:
                sub = re.findall(r'\S*', sub)
                sub = "r/" + sub[0] if sub[0:2] != "r/" else sub[0]
                url = "http://www.reddit.com/" + sub + "/.json?limit=6"
                subreddit = "http://www.reddit.com/" + sub
                request = requests.get(url, headers={'User-agent': 'testscript by /u/fakebot3'})
                data = request.json()
                posts = ""
                if request.status_code == 200:
                    for post in data['data']['children']:
                        domain = post['data']['domain']
                        title = treatTitle(post['data']['title'])
                        pUrl = urllib.parse.quote_plus(post['data']['url'])
                        isNsfw_bool = post['data']['over_18']
                        permalink = "http://www.reddit.com" + post['data']['permalink']
                        if isNsfw_bool:
                            isNsfw = "nsfw"
                        else:
                            isNsfw = "sfw"
                        post = u"`> `[{title}]({pUrl})` <{nsfw}> - `[comments]({permalink})\n".format(title=title,
                                                                                                      permalink=permalink,
                                                                                                      nsfw=isNsfw,
                                                                                                      pUrl=pUrl,
                                                                                                      domain=domain)
                        posts += post
                    if posts:
                        bot.sendMessage(msg['chat']['id'],
                                        u"[{sub}]({subreddit})`:`\n\n".format(sub=sub, subreddit=subreddit) + posts,
                                        reply_to_message_id=msg['message_id'], parse_mode="Markdown",
                                        disable_web_page_preview=True)
                    else:
                        bot.sendMessage(msg['chat']['id'], u"`I couldnt find {sub}, please try again`".format(sub=sub),
                                        reply_to_message_id=msg['message_id'], parse_mode="Markdown",
                                        disable_web_page_preview=True)
                elif request.status_code == 403:
                    bot.sendMessage(msg['chat']['id'], "`Subreddit not found, please verify your input.`",
                                    reply_to_message_id=msg['message_id'], parse_mode="Markdown")
                else:
                    bot.sendMessage(msg['chat']['id'],
                                    "`There has been an error, the number {error} to be specific.`".format(
                                        error=request.status_code), reply_to_message_id=msg['message_id'],
                                    parse_mode="Markdown")
            else:
                bot.sendMessage(msg['chat']['id'],
                                "`Follow this command with the name of a subreddit to see the top 6 posts.\nExample: /r Awww`",
                                reply_to_message_id=msg['message_id'], parse_mode="Markdown")
