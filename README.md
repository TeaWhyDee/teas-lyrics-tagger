Tag music files using Genius API (or manually).
Supports most audio formats (using [music-tag](https://github.com/KristoforMaynard/music-tag) library).  
Uses [wrap-genius](https://github.com/fedecalendino/wrap-genius) for genius API code.

You will need a Genius API key to use the functionality: https://docs.genius.com/

This script attempts ro remove genius artifacting (links etc.)
that sometimes appear in API responces.


# Requirements
Install dependencies in requirements.txt.

Tested with Python 3.11.5, 3.15.

# Run
Run `python main.py -h` for options.
```bash
usage: main.py [-h] [-t TOKEN] [-s SEARCH_STRING] [-l LYRICS] [-m] [-f] [-y]
               files [files ...]
```

There is an extra script `print_tag.py` for printing all or individual tags.

# Development
Create virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```


