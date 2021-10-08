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
		# Todo: users could be extended to be a class, to allow different users to track different stocks
		for user in defines.get("PM_LIST"):
			users.append(await client.fetch_user(user))

		data = analyzer.run_analysis()

		logger.info(f"Data: {data}")
		logger.info("Sending out data")

		formatted_stocks_data = "\n".join([data_ for data_ in data])

		# todo: this should be refactored, pure spaghetti

		text = f"""
			S&P 500 NH-NL: {analyzer.get_snp500_nh_nl_data()} ({analyzer.get_yesterdays_nhnl()}) \n\n
			Trade Ideas: \n{formatted_stocks_data}\n\n
		"""

		data_embed = discord.Embed(title="Daily Report", description=text, colour=discord.Colour(0x3239dc))

		for user in users:
			await user.send(embed=data_embed)

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
