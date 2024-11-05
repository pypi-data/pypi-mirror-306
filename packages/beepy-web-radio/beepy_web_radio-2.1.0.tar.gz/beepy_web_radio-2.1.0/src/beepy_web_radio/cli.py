import argparse
import logging
import sys
import traceback

from beepy_web_radio.api import get_stations, play_station, stop_playback

logger = logging.getLogger(__name__)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler("/tmp/beepy_web_radio.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Stream handler (for stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter("%(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)


def search_stations(query: str):
    try:
        stations = get_stations(query)
        if stations:
            logger.info(f"Found {len(stations)} stations:")
            for station in stations:
                logger.info(
                    f"- {station['title']} - {station['subtitle']} "
                    f"({station['stream']})"
                )
        else:
            logger.info("No stations found matching the query.")
    except Exception as e:
        logger.error(f"Error searching for stations: {e}")


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Beepy Web Radio CLI")
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )

    search_parser = subparsers.add_parser("search", help="Search for stations")
    search_parser.add_argument(
        "query", nargs="+", help="Search query (can be multiple words)"
    )

    play_parser = subparsers.add_parser("play", help="Play a station")
    play_parser.add_argument("station", nargs="+", help="Station URL to play")

    subparsers.add_parser("stop", help="Stop playback")

    args = parser.parse_args()

    try:
        if args.command == "search":
            query = " ".join(args.query)
            search_stations(query)
        elif args.command == "play":
            station = " ".join(args.station)
            play_station(station)
        elif args.command == "stop":
            stop_playback()
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.error("Detailed exception information:")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
