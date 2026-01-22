import argparse
import os
import re
import sys
from typing import List

import music_tag
from lyricsgenius import Genius


def parse_arguments():
    parser = argparse.ArgumentParser(description="Tagger")

    parser.add_argument("files", nargs="+", help="Path(s) to file(s)")
    parser.add_argument("-t", "--token", type=str, help="Genius token")
    parser.add_argument("-s", "--search_string", type=str, help="Search string")
    parser.add_argument("-l", "--lyrics", type=str, help="Lyrics to put")
    parser.add_argument("-m", "--manual", action="store_true", help="Tag manally")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Add or replace lyrics even if lyrics tag is already present",
    )
    parser.add_argument(
        "-y",
        "--always_yes",
        action="store_true",
        help="Save the lyrics without asking the user if they're correct",
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


def get_search_string(file, path, force=False):
    title = file["title"]
    album = file["album"]
    artist = file["artist"]

    if file["lyrics"] and not force:
        # print(file['lyrics'])
        return None

    if not title:
        return os.path.splitext(os.path.basename(path))[0]

    return f"{artist} {title}"


def find_song(search_string: str, genius_client):
    song = genius_client.search_song(search_string)

    try:
        return song
    except StopIteration:
        return None


def main():
    unfound_songs: List = []

    args = parse_arguments()

    files = args.files
    for filepath in files:
        f = music_tag.load_file(filepath)

        content = ""
        if args.manual:  # MANUAL
            song_name = get_search_string(f, filepath, args.force)
            print(filepath)
            print(song_name)

            for line in sys.stdin:
                content += line
                if line == "":
                    break

            print("--- Saving provided lyrics..")
            lyrics = content

        else:  # NON MANUAL
            g = Genius(args.token)
            if not args.search_string:
                search_string = get_search_string(f, filepath, args.force)
            else:
                search_string = args.search_string

            if not search_string:
                print("--- Skipping", filepath)
                continue

            print("Search string:", search_string)
            if args.lyrics:
                lyrics = args.lyrics
            else:
                song = find_song(search_string, g)
                if not song:
                    unfound_songs.append(search_string)
                    continue
                lyrics = "\n".join(song.lyrics.split("\n")[1:]).strip()
                lyrics = lyrics.replace("You might also like", "")

                # remove Genius artifact
                lyrics = re.sub(r"\d*Embed$", "", lyrics)

                print(
                    f"----- Found song: {song.artist} - {song.title} \n\t {'\n'.join(lyrics.split("\n"))} \n"
                )
                print("--- Are these correct? [<ctrl-d>=yes, input=correct lyrics] ")

                for line in sys.stdin:
                    content += line
                    if line == "":
                        break

                if content == "":
                    print("--- Saving the found lyrics..")
                else:
                    print("--- Saving provided lyrics..")
                    lyrics = content
                print()
                print("=========================")

        f["lyrics"] = lyrics
        f.save()

    print()
    for i in unfound_songs:
        print(f"--- Couldn't find song: {i}")


if __name__ == "__main__":
    main()
