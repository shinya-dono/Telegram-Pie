# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from pyrogram import Client
import asyncio
import time
import arabic_reshaper

from bidi.algorithm import get_display



def make_farsi_text(x):
	reshaped_text = arabic_reshaper.reshape(x)
	farsi_text = get_display(reshaped_text)
	return farsi_text

loop = asyncio.get_event_loop()
async def main():

	acc = input("please enter a name: ")
	counts = []
	names = []
	total = 0
	api_id = int(input("please enter your API ID: "))
	api_hash = input("please enter your API HASH: ")
	app = Client(acc, api_id, api_hash)
	await app.start()
	contacts = await app.get_contacts()
	for user in contacts:
		try:
			count = await app.get_history_count(user.id)
		except FloodWait as e:
			time.sleep(e.x)
		total += count
		if count < 1000:
			continue
		names.append(user.first_name)
		counts.append(count)
		

	patches, text= plt.pie(counts, startangle=90)
	plt.rc('font', family='Arial')
	plt.legend(patches, labels=['%s: %1.1f %%  (%s)' % (make_farsi_text(l), (s/total)*100, "{:,}".format(s)) for l, s in zip(names,counts)], loc="best")
	plt.axis('equal')
	plt.title("{:,} messages in total".format(total))
	plt.tight_layout()
	plt.savefig(f"{acc}.jpg", format='jpg')

loop.run_until_complete(main())
