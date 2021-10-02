from loguru import logger
import pathlib, json


PATH = "res/defines.json"


__defines = {

}

__initialized = [False]


def init():
	if not __initialized[0]:
		logger.info("Loading defines")

		try:
			with open(pathlib.Path(PATH)) as config_file:
				config = json.load(config_file)

			for configuration in config:
				__defines.update({configuration: config[configuration]})
		except FileNotFoundError:
			logger.error("config.json not found")

		__initialized[0] = True


def get(name):
	if __initialized[0]:
		return __defines[name]
	else:
		raise NotImplementedError("Attempted to access defines before initializing")
