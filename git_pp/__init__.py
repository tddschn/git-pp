__version__ = '1.9.5'
__app_name__ = 'git pp'

try:
	from logging_utils_tddschn import get_logger # type: ignore
	logger, _ = get_logger(__app_name__)
except:
	import logging
	from logging import NullHandler
	logger = logging.getLogger(__name__)
	logger.addHandler(NullHandler())