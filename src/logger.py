from loguru import logger


PATH = "logs/"


def init():
	logger.info("Resetting latest.log")

	# TODO: Reset latest.log using os to delete the file

	logger.add(f"{PATH}main.log", rotation="10 MB")
	logger.add(f"{PATH}latest.log")
	logger.add(f"{PATH}errors.log", level="ERROR", rotation="5 MB")
	logger.info("Logger initialised")


if __name__ == "__main__":
	PATH = "../logs/"
	init()
