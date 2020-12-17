# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pyrogram import Client
import asyncio
import time
import arabic_reshaper
from datetime import datetime
from pyrogram.errors import FloodWait
from bidi.algorithm import get_display


def make_farsi_text(x):
    reshaped_text = arabic_reshaper.reshape(x)
    farsi_text = get_display(reshaped_text)
    return farsi_text


loop = asyncio.get_event_loop()


async def main():
    acc = "shinya"
    data = []
    total = 0
    api_id = 966253
    api_hash = "e21862b4ea068f9067c2749c06430a7c"
    app = Client(acc, api_id, api_hash)
    await app.start()
    contacts = await app.get_contacts()
    for user in contacts:
        try:
            count = await app.get_history_count(user.id)
            first = await app.get_history(user.id, 2, count - 1)
        except FloodWait as e:
            time.sleep(e.x)
        total += count
        if count < 1000:
            continue
        date_time_obj = datetime.fromtimestamp(first[0].date)
        data += [(user.first_name, count, (datetime.now() - date_time_obj).days)]

    data = sorted(data, key=lambda x: x[1], reverse=True)
    patches, text = plt.pie([y for x, y, z in data], startangle=90)
    plt.rc('font', family='Arial')
    plt.legend(patches,
               labels=['%s: %1.1f %%(%s) - %d per day' % (
               make_farsi_text(l), (s / total) * 100, "{:,}".format(s), (s / z)) for l, s, z in
                       data], loc="best")
    plt.axis('equal')
    plt.title("{:,} messages in total".format(total))
    plt.tight_layout()
    plt.savefig(f"{acc}.jpg", format='jpg')


loop.run_until_complete(main())
