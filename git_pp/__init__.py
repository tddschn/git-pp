__version__ = '1.9.3'
__app_name__ = 'git pp'

try:
	from logging_utils_tddschn import get_logger # type: ignore
	logger, _ = get_logger(__app_name__)
except:
	# try:
	#     from loguru import logger  # type: ignore
	#     logger.disable(__name__)
	# except:
	import logging
	from logging import NullHandler
	# logging.basicConfig(level=logging.NOTSET)
	logger = logging.getLogger(__name__)
	logger.addHandler(NullHandler())
	logger.setLevel(logging.INFO)