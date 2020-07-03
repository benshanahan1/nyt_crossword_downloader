# NYT Crossword Downloader

Download NYT crossword puzzle JSON data.

**NOTE:** Without a [NYT crossword subscription](https://www.nytimes.com/subscription/crosswords), you will only be able to access meta-information about the crosswords (e.g. title, date, author, etc.). In order to get the actual puzzle data, you will need a paid subscription. See the [Cookies section below](#cookies) for information on how to download your browser cookies.

## Installation

```bash
pip install git+https://github.com/benshanahan1/nyt_crossword_downloader
```

## Usage

```text
$ nyt_crossword_downloader --help
usage: nyt_crossword_downloader [-h] [--cookies COOKIES] [--date DATE]
                                [--puzzle-id PUZZLE_ID] [--date-folders]
                                destination

Download NYT crossword puzzles.

positional arguments:
  destination           Folder where crossword data will be written.

optional arguments:
  -h, --help            show this help message and exit
  --cookies COOKIES, -c COOKIES
                        NYT cookies.txt file for authentication.
  --date DATE, -d DATE  Download a puzzle from a particular date.
  --puzzle-id PUZZLE_ID, -p PUZZLE_ID
                        Download a particular puzzle ID.
  --date-folders        Place downloaded puzzles into folders organized by
                        year and month. Default is completely flat folder
                        structure.
```

CLI examples:

```bash
# download today's puzzle meta (no auth required)
nyt_crossword_downloader ~/puzzles/

# download today's puzzle
nyt_crossword_downloader ~/puzzles/ --cookies ~/cookies.txt

# download puzzle from 1/1/2000
nyt_crossword_downloader ~/puzzles/ --cookies ~/cookies.txt --date 2000-01-01
```

The `RangeDownloader` class can be used to download a date range of puzzles all at once, e.g.:

```python
from nyt_crossword_downloader import RangeDownloader
from datetime import datetime

r = RangeDownloader(
    "~/puzzles",
    "~/cookies.txt",
    date_folders=True,
    secs_btwn_queries=10,
)
date_start = datetime(2020, 1, 1)
date_stop = datetime(2020, 1, 31)
r.download_date_range(date_start, date_stop)
```

## Cookies

In order to use this tool, you need to download your NYT cookies (information stored in your web browser that tells NYT's servers that you're logged into your account). The steps are as follows:

1. Navigate to the [NYT crosswords page](https://nytimes.com/crosswords) and login.
2. Use the [cookies.txt Chrome extension](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en) to download your cookies and place the file somewhere secure on your computer.
