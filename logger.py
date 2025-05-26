import logging

logging.basicConfig(level=logging.INFO, filename="project.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
