import argparse
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
    elif mode == "threading":
        threads_main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bus_data Crawler")
    parser.add_argument("--mode", type=str, default="threading", help="Execution mode (sequential, async, threading)")
    args = parser.parse_args()

    mode = args.mode.lower()
    if mode not in ["sequential", "async", "threading"]:
        raise ValueError("Invalid mode. Choose from: sequential, async, threading")

    main(mode)
