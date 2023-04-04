import sys

MIN_VER = (3, 11)

try:
  import main
except ImportError:
  input("This game requires Pygame and Shapely. Run `pip install -r requirements.txt` to install them. If this error persists, the game folder might be missing some files. In this case, try redownloading the game. Press ENTER to exit...".format(*MIN_VER))
  sys.exit()

if sys.version_info[:2] < MIN_VER:
  input("This game requires Python {}.{}. Press ENTER to exit...".format(*MIN_VER))
  sys.exit()
else:
  main.main()
