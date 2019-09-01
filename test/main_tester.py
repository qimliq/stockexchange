import logging
from src.book_keeper import BookKeeper

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating keeper")

    keeper = BookKeeper("test")

    logging.info("Main    : all done")


