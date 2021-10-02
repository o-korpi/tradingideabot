from asyncio import AbstractEventLoop

from loguru import logger
from src import defines
from src.data import analyzer
import discord
import asyncio


logger.info("Initiating discord client")
activity = discord.Game("Sending trade ideas")
client = discord.Client(activity=activity)
users = []


def init():
	logger.info("Starting bot...")

	logger.info("Setting prefix status")

	@client.event
	async def on_ready():
		logger.info('We have logged in as {0.user}'.format(client))

		logger.info("Preparing PM list")
		for user in defines.get("PM_LIST"):
			users.append(await client.fetch_user(user))

		data = analyzer.run_analysis()

		logger.info(f"Data: {data}")
		logger.info("Sending out data")
		for data_ in data:
			for user in users:
				# await asyncio.sleep(0.33)  # not necessary?
				await user.send(data_)

		if len(data) == 0:
			for user in users:
				await user.send("No new trades today")
		await client.close()

	token = defines.get("TOKEN")
	if len(token) == 0:
		logger.error("Invalid Token: Token must not be empty! Fix this in config.json")
		quit()

	logger.info("Running bot...")

	async def client_start():
		await client.start(token)

	loop = asyncio.get_event_loop()
	coroutine = client_start()
	loop.run_until_complete(coroutine)
