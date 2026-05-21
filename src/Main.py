## @file   Main.py
#  @brief  Generates a worship chart from specified songs and keys.
#  @author Samuel Crawford
#  @date   5/21/2026

from GUI import songGUI, statusGUI


## @brief The main function of the program that calls other programs.
def main():
    # Get list of songs, keys, and output filename from user
    songs, keys, filename = songGUI()

    # Pass these arguments to be processed and displayed on status GUI
    statusGUI(songs, keys, filename)


if __name__ == "__main__":
    main()
