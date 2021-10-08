from loguru import logger as lgr
from src import logger, defines
from src.bot import bot


def run(event, context):
	lgr.info("Starting")
	logger.init()
	defines.init()
	bot.init()


if __name__ == '__main__':
	run(0, 0)
