import logging

logger = logging.getLogger("hebergement")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Ajouter le handler au logger s’il n’est pas déjà là
if not logger.hasHandlers():
    logger.addHandler(console_handler)
