import shutil
import sys
from pathlib import Path

import manage

HOME_SASS_SOURCE_DIR = "home/static/home/scss"
HOME_SASS_TARGET_DIR = "home/static/home/css"

def main() -> None:
    shutil.rmtree(HOME_SASS_TARGET_DIR, ignore_errors=True)
    Path(HOME_SASS_TARGET_DIR).mkdir(parents=True, exist_ok=True)
    sys.argv.append("sass")
    sys.argv.append(HOME_SASS_SOURCE_DIR)
    sys.argv.append(HOME_SASS_TARGET_DIR)
    manage.main(sys.argv)


if __name__ == "__main__":
    main()
