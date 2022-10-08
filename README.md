# Python YT to MP3
This is a project that heavily relies on [Pytub](https://github.com/pytube/pytube)

## How to use
You will need the folowing instalations :
- Python 3 ([Windows](https://www.python.org/downloads/windows/), [MacOS](https://www.python.org/downloads/macos/))<br>
- pip ([Windows](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/), [MacOS](https://www.geeksforgeeks.org/how-to-install-pip-in-macos/))<br>
- [FFMPEG](https://ffmpeg.org/download.html) (use Brew on mac ``brew install ffmpeg``)
- ``pip install pytube``

then you need to modify the program :
- ``musicFolder`` should be a string to wherever you want to store music
- create a rapid api acount(s), get a 0$ plan at https://rapidapi.com/apidojo/api/shazam/pricing
- get the api key from https://rapidapi.com/developer/dashboard -> your default app -> security
- paste the key(s) in ``APIkey`` (keep it as a list)

To use, open a terminal and execute the programe with ``python [path to program]/YT-MP3_clasification.py`` and type the video or playlist URL.

## Improvement to come
- Easier instalation
- Linux compatibility
- Multithreading for playlist download
- More user friendly interface
