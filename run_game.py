import sys
from main import main

MIN_VER = (3, 11)

if sys.version_info[:2] < MIN_VER:
  input("This game requires Python {}.{}. Press ENTER to exit...".format(*MIN_VER))
  sys.exit()
else:
  main()