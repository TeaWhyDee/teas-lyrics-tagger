import argparse
import os
import re
import sys
from typing import List

import music_tag
from lyricsgenius import Genius


class NoGeniusSongFound(Exception):
    def __init__(self, message, search_string):
        super().__init__(message)
        self.search_string = search_string


class LyricsTagPresent(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="\
Audio file lyrics tagger. \
This script will extract the artist and track names, \
look them up on Genius and set the 'lyrics' metadata tag.\
"
    )

    parser.add_argument("files", nargs="+", help="path(s) to file(s)")
    parser.add_argument("-t", "--token", type=str, help="Genius token")
    parser.add_argument(
        "-s",
        "--search_string",
        type=str,
        help="specify the Genius API search string (usually 'artist track_title')",
    )
    parser.add_argument(
        "-l", "--lyrics", type=str, help="set the provided lyrics non-interactively"
    )
    parser.add_argument(
        "-m",
        "--manual",
        action="store_true",
        help="manual interactive mode. Manually set lyrics to one or multiple files",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="add/replace lyrics tag even the tag is already present",
    )
    parser.add_argument(
        "-y",
        "--always_yes",
        action="store_true",
        help="save the lyrics without asking the user first",
    )

    args = parser.parse_args()
    env_token = os.environ.get("GENIUS_TOKEN")
    if env_token:
        args.token = env_token

    if not args.token and not args.manual:
        print("Please provide Genius API token.")
        print("https://genius.com/api-clients")
        exit(1)

    return args


def get_search_string(file, path, force):
    title = file["title"]
    album = file["album"]
    artist = file["artist"]

    if file["lyrics"] and not force:
        raise LyricsTagPresent("")

    if not title:
        return os.path.splitext(os.path.basename(path))[0]

    return f"{artist} {title}"


def get_song_genius(search_string: str, genius_client: Genius):
    """
    Search song with genius
    """
    song = genius_client.search_song(search_string)

    try:
        return song
    except StopIteration:
        return None


def tag_manual(f, filepath, args):
    content = ""

    song_name = get_search_string(f, filepath, args.force)
    print(f"Path: {filepath}")
    print(f"Song: {song_name}")
    print("--- Provdide lyrics (finish with <ctrl-d>):")

    for line in sys.stdin:
        content += line

    print("--- Saving provided lyrics..")

    content = content.strip()
    return content


def tag_auto(f, filepath, args):
    content = ""

    g = Genius(args.token, verbose=False)
    if not args.search_string:
        search_string = get_search_string(f, filepath, args.force)
    else:
        search_string = args.search_string

    if not search_string:
        print("--- Skipping", filepath)
        raise NoGeniusSongFound("Cannot get search string", "")

    # Access Genius API
    print("--- Search string:", search_string)
    song = get_song_genius(search_string, g)
    if not song:
        raise NoGeniusSongFound("", search_string)

    lyrics = "\n".join(song.lyrics.split("\n")[1:])

    # remove Genius artifacts
    lyrics = lyrics.replace("You might also like", "")
    lyrics = re.sub(r"\d*Embed$", "", lyrics)
    lyrics = lyrics.strip()

    print(f'--- Found song "{song.artist} - {song.title}" with lyrics:')
    print(f'{"\n".join(lyrics.split("\n"))} \n')

    # Interactive mode prompt
    if not args.always_yes:
        print("--- Are these lyrics correct? [<ctrl-d>=yes, input=correct lyrics] ")

        for line in sys.stdin:
            content += line
            if line == "":
                break

    if content == "":
        print("--- Saving found lyrics")
    else:
        print("--- Saving provided lyrics")
        lyrics = content

    return lyrics


def main():
    args = parse_arguments()
    unfound_songs: List = []

    files = args.files
    try:
        for filepath in files:
            print("=============================")
            print(filepath)

            f = music_tag.load_file(filepath)

            if args.lyrics:
                print("--- Saving provided lyrics..")
                lyrics = args.lyrics

            else:
                if args.manual:
                    lyrics = tag_manual(f, filepath, args)
                else:
                    try:
                        lyrics = tag_auto(f, filepath, args)
                    except NoGeniusSongFound as e:
                        unfound_songs.append(e.search_string)
                        continue
                    except LyricsTagPresent as e:
                        print("--- Lyrics tag already preset, skipping.")
                        continue
            print()

            f["lyrics"] = lyrics
            f.save()

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting.")

    finally:
        if unfound_songs:
            print("--- Errors ---")
            for i in unfound_songs:
                print(f"--- Couldn't find song: {i}")


if __name__ == "__main__":
    main()
