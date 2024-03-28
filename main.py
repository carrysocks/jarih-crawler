import asyncio
import logging

from async_main import async_main
from sequential_main import seqeuntial_main
from threads_main import threads_main


def main(mode):

    if mode == "sequential":
        seqeuntial_main()
    elif mode == "async":
        asyncio.run(async_main())
    elif mode == "threads":
        threads_main()
    else:
        raise ValueError("Invalid mode")


if __name__ == "__main__":
    try:
        modes = ["sequential", "async", "threads"]
        mode = modes[2]
        main(mode)
    except Exception as e:
        logging.error(f"Error in main: {e}")
