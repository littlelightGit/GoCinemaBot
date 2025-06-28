import logging

logging.basicConfig(level=logging.INFO, filename="project.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
