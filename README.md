# Crossword Downloader

Download NYT crossword puzzles in JSON format.

**NOTE:** This tool requires that you have a [NYT crossword subscription](https://www.nytimes.com/subscription/crosswords).

## Installation

```bash
pip install git+https://github.com/benshanahan1/crossword_downloader
```

## Usage

```text
$ crossword_downloader --help
usage: crossword_downloader [-h] [--date DATE] [--puzzle-id PUZZLE_ID]
                            [--download-type {json,puz}]
                            cookies destination

Download NYT crossword puzzles.

positional arguments:
  cookies               NYT cookie text file.
  destination           Folder where crossword data will be written.

optional arguments:
  -h, --help            show this help message and exit
  --date DATE, -d DATE  Date to download.
  --puzzle-id PUZZLE_ID, -p PUZZLE_ID
                        Puzzle ID to download.
  --download-type {json,puz}
                        Type of download, JSON or PUZ.
```

Examples:

```bash
# download today's puzzle in json format
crossword_downloader ~/desktop/nyt-cookie.txt ~/desktop/puzzles

# download today's puzzle in puz format
crossword_downloader ~/desktop/nyt-cookie.txt ~/desktop/puzzles --download-type puz

# download puzzle from Jan 1, 2000
crossword_downloader ~/desktop/nyt-cookie.txt ~/desktop/puzzles --date 2000-01-01

# download puzzle with ID 4111
crossword_downloader ~/desktop/nyt-cookie.txt ~/desktop/puzzles --puzzle-id 4111
```
