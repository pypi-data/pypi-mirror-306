import logging
import subprocess
from typing import Dict, List, Optional
from urllib.parse import urlparse

import psutil
import requests

logger = logging.getLogger(__name__)


def get_current_station() -> Optional[str]:
    for proc in psutil.process_iter(["name", "cmdline"]):
        if proc.info["name"] == "mpv":
            cmdline = proc.info["cmdline"]
            for i, arg in enumerate(cmdline):
                if arg.startswith("--title="):
                    return str(
                        arg[8:]
                    )  # Return the title without the '--title=' prefix
                elif arg == "--title" and i + 1 < len(cmdline):
                    return str(
                        cmdline[i + 1]
                    )  # Return the next argument after '--title'
    return None


def get_stations(query: str) -> List[Dict]:
    url = "https://radio.garden/api/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    filtered_stations = [
        station
        for station in data["hits"]["hits"]
        if station["_source"]["type"] == "channel" and station["_score"] > 50
    ]

    return [
        {
            "title": station["_source"]["title"],
            "subtitle": station["_source"]["subtitle"],
            "stream": station["_source"]["stream"],
            "score": station["_score"],
        }
        for station in filtered_stations
    ]


def play_station(station: str, station_title: Optional[str] = None):
    logger.info(f"Attempting to play: {station}")

    # Stop any currently playing station
    stop_playback()

    # Simple URL validation
    parsed_url = urlparse(station)
    if parsed_url.scheme and parsed_url.netloc:
        url_to_play = station
    else:
        # If not a URL, use it as a search query
        try:
            stations = get_stations(station)
            if stations:
                # Sort stations by score in descending order and get the
                # highest scoring one
                highest_scoring_station = max(
                    stations,
                    key=lambda x: x["score"],
                )
                url_to_play = highest_scoring_station["stream"]
                station_title = highest_scoring_station["title"]
                logger.info(
                    f"Playing highest scoring station: "
                    f"{highest_scoring_station['title']}"
                )
            else:
                logger.info("No stations found matching the query.")
                return
        except requests.RequestException as e:
            logger.error(f"Error searching for stations: {e}")
            return

    try:
        # Run mpv command as a background process that continues after the
        # script exits
        subprocess.Popen(
            f"nohup sh -c 'mpv --no-video {url_to_play} "
            f'--title="{station_title}"\' > /dev/null 2>&1 &',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info(f"Started playback of {station_title} ({url_to_play})")
    except subprocess.SubprocessError as e:
        logger.error(f"Error starting playback: {e}")


def stop_playback():
    logger.info("Stopping playback")
    current_station = get_current_station()
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == "mpv":
            proc.terminate()
            logger.info(f"Stopped mpv process playing: {current_station}")
    logger.info("Playback stopped")
