## @file   CommonSections.py
#  @brief  Finds the most common section names from song files.
#  @author Samuel Crawford
#  @date   4/27/2026


from pathlib import Path

from Helpers import getSetting, getValidSongs
from collections import defaultdict


## @brief A helper function that prints the most common section names found in song files.
def main():
    sections = defaultdict(int)

    for s in getValidSongs():
        songPath = Path(getSetting("SONG_PATH"))
        with open(songPath / f"{s}.txt", "r") as fp:
            contents = fp.readlines()
        for i in contents[1:]:
            sections[i.split(":")[0]] += 1

    for k, v in sorted(sections.items(), key=lambda kv: kv[1], reverse=True):
        print(k, v)


if __name__ == "__main__":
    main()
