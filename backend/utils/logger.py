import logging
import sys

# Configure standard formatting for logging
logging_format = (
    "[%(asctime)s] %(levelname)s in %(module)s (Line %(lineno)d): %(message)s"
)

logging.basicConfig(
    level=logging.INFO,
    format=logging_format,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("terrava")
