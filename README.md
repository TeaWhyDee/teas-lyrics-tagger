Tag music files using Genius API (or manually).
Supports most audio formats (using [music-tag](https://github.com/KristoforMaynard/music-tag) library).  
Thanks to [wrap-genius](https://github.com/fedecalendino/wrap-genius) for genius API code.

This script attempts ro remove genius artifacting (links etc.)
that sometimes appear in API responces.


# Requirements
Dependencies in requirements.txt.
Tested with Python 3.11.5, 3.15.

# Run
```bash
usage: main.py [-h] [-t TOKEN] [-s SEARCH_STRING] [-l LYRICS] [-m] [-f] [-y]
               files [files ...]
```

# Develop
Create virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```


