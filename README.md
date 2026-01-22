Tag music files using Genius API (or manually).
Supports most audio formats (using [music-tag](https://github.com/KristoforMaynard/music-tag) library).
Uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) for genius API code.

This script attempts ro remove Genius artifacting (links etc.)
that sometimes appear in API responces.

You will need a Genius API key to use the search functionality:
https://docs.genius.com/


# Requirements
Install dependencies in requirements.txt.

Tested with Python 3.11.5, 3.15.

# Run
The script will run in an interactive mode by default.
The script will always skip a file if the lyrics tag is already set,
unless the force option is specified.

Run `python main.py -h` for options.
```bash
usage: main.py [-h] [-t TOKEN] [-s SEARCH_STRING] [-l LYRICS] [-m] [-f] [-y]
               files [files ...]
               
positional arguments:
  files                 path(s) to file(s)

options:
  -h, --help            show this help message and exit
  -t, --token TOKEN     Genius token
  -s, --search_string SEARCH_STRING
                        specify the Genius API search string (usually 'artist track_title')
  -l, --lyrics LYRICS   set the provided lyrics non-interactively
  -m, --manual          manual interactive mode. Manually set lyrics to one or multiple files
  -f, --force           add/replace lyrics tag even the tag is already present
  -y, --always_yes      save the lyrics without asking the user first
```

Example usage `python main.py -t $GENIUS_TOKEN ./file.mp3 -s "Kkaydes For What"`:
```bash
./file.mp3
--- Search string: Kkaydes For What
--- Found song "Kkaydes - For What" with lyrics:
For what?

--- Are these lyrics correct? [<ctrl-d>=yes, input=correct lyrics]
These are manually typed lyrics.
--- Saving provided lyrics
```

There is an extra script `print_tag.py` for printing all or individual tags.

# Development
This codebase uses exceptions for flow control, yikes!

Create virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```


