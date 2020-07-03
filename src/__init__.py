"""
there are two rate limits per API: 4,000 requests per day and 10 requests per
minute. You should sleep 6 seconds between calls to avoid hitting the per
minute rate limit.
"""


import requests
import os
import json
from datetime import datetime
from dateutil.parser import parse as parse_dt_str
from argparse import ArgumentParser


def build_parser():
    today = datetime.now().strftime("%Y-%m-%d")
    parser = ArgumentParser(description="Download NYT crossword puzzles.")
    parser.add_argument("cookies", help="NYT cookie text file.")
    parser.add_argument(
        "destination", help="Folder where crossword data will be written."
    )
    parser.add_argument("--date", "-d", default=today, help="Date to download.")
    parser.add_argument("--puzzle-id", "-p", type=int, help="Puzzle ID to download.")
    parser.add_argument(
        "--download-type",
        choices=["json", "puz"],
        default="json",
        help="Type of download, JSON or PUZ.",
    )
    return parser


def get_puzzle_id_by_date(dt):
    d = dt.strftime("%Y-%m-%d")
    url = f"https://nyt-games-prd.appspot.com/svc/crosswords/v3/36569100/puzzles.json?publish_type=daily&sort_order=asc&sort_by=print_date&date_start={d}&date_end={d}"
    resp = requests.get(url)
    try:
        resp_json = resp.json()
        return resp_json["results"][0]["puzzle_id"]
    except Exception:
        return None


def load_cookie_from_file(cookie_file):
    with open(cookie_file, "r") as fd:
        return str(fd.read()).rstrip()


def get_puzzle_json_by_puzzle_id(puzzle_id, cookie_file, download_type):
    url = (
        f"https://www.nytimes.com/svc/crosswords/v2/puzzle/{puzzle_id}.{download_type}"
    )
    headers = {"cookie": load_cookie_from_file(cookie_file)}
    print(f"Downloading puzzle {puzzle_id}")
    resp = requests.get(url, headers=headers)
    return resp.json()


def get_puzzle_title(puzzle_id, data):
    results = data["results"]
    if len(results) == 1:
        try:
            return data["results"][0]["puzzle_meta"]["printDate"]
        except Exception:
            pass
    return str(puzzle_id)


def write_puzzle_to_disk(puzzle_id, data, destination, download_type):
    filename = get_puzzle_title(puzzle_id, data)
    path = os.path.join(destination, f"{filename}.{download_type}")
    with open(path, "w") as fd:
        json.dump(data, fd, indent=2)
    return path


def main():
    parser = build_parser()
    args = parser.parse_args()

    # If puzzle ID is not provided, download today's puzzle.
    if args.puzzle_id is None:
        parsed_date = parse_dt_str(args.date)
        puzzle_id = get_puzzle_id_by_date(parsed_date)
    else:
        puzzle_id = args.puzzle_id

    # Download the puzzle
    puzzle = get_puzzle_json_by_puzzle_id(puzzle_id, args.cookies, args.download_type)

    try:
        os.mkdir(args.destination)
    except FileExistsError:
        pass
    except Exception as error:
        print(f"Unable to create directory: {error}")
        exit(1)

    path = write_puzzle_to_disk(puzzle_id, puzzle, args.destination, args.download_type)
    print(f"Puzzle {puzzle_id} downloaded to: {path}")
