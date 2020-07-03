"""
there are two rate limits per API: 4,000 requests per day and 10 requests per
minute. You should sleep 6 seconds between calls to avoid hitting the per
minute rate limit.
"""


import requests
import os
import json
import re
from datetime import datetime
from dateutil.parser import parse as parse_dt_str
from argparse import ArgumentParser


class MissingPuzzleData(Exception):
    pass


class CLIArgs:
    def __init__(self):
        self.parser = self.build_parser()

    def parse(self):
        return self.parser.parse_args()

    def build_parser(self):
        today = Puzzle.format_date(datetime.now())
        parser = ArgumentParser(description="Download NYT crossword puzzles.")
        parser.add_argument("cookies", help="NYT cookie text file.")
        parser.add_argument(
            "destination", help="Folder where crossword data will be written."
        )
        parser.add_argument("--date", "-d", default=today, help="Date to download.")
        parser.add_argument(
            "--puzzle-id", "-p", type=int, help="Puzzle ID to download."
        )
        parser.add_argument(
            "--date-folders",
            action="store_true",
            help="Place downloaded puzzles into folders by year and month. Default is completely flat folder structure.",
        )
        return parser


class Puzzle:
    URL_RECENT_PUZZLES = "https://nyt-games-prd.appspot.com/svc/crosswords/v3/36569100/puzzles.json?publish_type=daily&sort_order=asc&sort_by=print_date&date_start={date_start}&date_end={date_end}"
    URL_PUZZLE_BY_ID = (
        "https://www.nytimes.com/svc/crosswords/v2/puzzle/{puzzle_id}.json"
    )

    def __init__(self, cookies):
        self.cookies = cookies

    def get_puzzle_id_by_date(self, dt):
        d = self.format_date(dt)
        url = self.URL_RECENT_PUZZLES.format(date_start=d, date_end=d)
        resp = requests.get(url)
        try:
            resp_json = resp.json()
            return resp_json["results"][0]["puzzle_id"]
        except Exception:
            return None

    def get_puzzle_date_str(self, data, day_only=False):
        if day_only:
            return self.zero_pad_two(self.get_puzzle_date(data).day)
        return self.get_puzzle_date(data, return_date_str=True)

    def get_puzzle_date(self, data, return_date_str=False):
        try:
            date_str = data["results"][0]["puzzle_meta"]["printDate"]
        except KeyError:
            raise MissingPuzzleData("No data could be found for this puzzle!")
        else:
            if return_date_str:
                return date_str
            return parse_dt_str(date_str)

    @classmethod
    def format_date(self, dt):
        return dt.strftime("%Y-%m-%d")

    @classmethod
    def zero_pad_two(self, n):
        return "{:02d}".format(n)

    def get_puzzle_data_by_date(self, dt):
        puzzle_id = self.get_puzzle_id_by_date(dt)
        _, _, data = self.get_puzzle_data_by_id(puzzle_id)
        return puzzle_id, dt, data

    def get_puzzle_data_by_id(self, puzzle_id):
        url = self.URL_PUZZLE_BY_ID.format(puzzle_id=puzzle_id)
        resp = requests.get(url, cookies=self.cookies.cookies)
        data = resp.json()
        return puzzle_id, self.get_puzzle_date(data), data


class Cookies:
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file

    @property
    def cookies(self):
        return self.parse(self.cookie_file)

    def parse(self, cookie_file):
        """Load and parse a cookies.txt file into a dict.

        Parse a cookies.txt file and return a dictionary of key value pairs
        compatible with requests.

        See: https://stackoverflow.com/a/54659484/5161222
        """
        cookies = {}
        with open(cookie_file, "r") as fd:
            for line in fd:
                if not re.match(r"^\#", line):
                    line_fields = line.strip().split("\t")
                    cookies[line_fields[5]] = line_fields[6]
        return cookies


class FileSystem:
    def __init__(self, puzzle, destination_folder, date_folders=False):
        self.puzzle = puzzle
        self.destination = destination_folder
        self.date_folders = date_folders

    def get_destination_root(self, dt=None):
        if self.date_folders:
            return os.path.join(
                self.destination, str(dt.year), self.puzzle.zero_pad_two(dt.month)
            )
        else:
            return self.destination

    def make_destination_folder_if_not_exists(self, dt):
        try:
            root = self.get_destination_root(dt)
            os.makedirs(root, exist_ok=True)
        except Exception as error:
            raise Exception(f"Cannot create destination directory: {error}")
        else:
            return root

    def write_to_disk(self, puzzle_id, dt, data):
        root = self.make_destination_folder_if_not_exists(dt)
        filename = self.puzzle.get_puzzle_date_str(data, day_only=self.date_folders)
        path = os.path.join(root, f"{filename}.json")
        with open(path, "w") as fd:
            json.dump(data, fd, indent=2)
        return path


def main():
    args = CLIArgs().parse()
    cookies = Cookies(args.cookies)
    puzzle = Puzzle(cookies)
    file_system = FileSystem(puzzle, args.destination, args.date_folders)

    if args.puzzle_id is None:
        puzzle_id, puzzle_date, puzzle_data = puzzle.get_puzzle_data_by_date(
            parse_dt_str(args.date)
        )
    else:
        puzzle_id, puzzle_date, puzzle_data = puzzle.get_puzzle_data_by_id(
            args.puzzle_id
        )

    # Write puzzle to disk.
    path = file_system.write_to_disk(puzzle_id, puzzle_date, puzzle_data)
    puzzle_date_str = puzzle.format_date(puzzle_date)
    print(f"Downloaded {puzzle_date_str} puzzle (ID: {puzzle_id}) to: {path}")
