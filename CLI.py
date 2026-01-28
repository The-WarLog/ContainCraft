import sys
import os
from containcraft.cli import main
# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))



if __name__ == "__main__":
    main()
