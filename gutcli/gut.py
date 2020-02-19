import argparse
import subprocess
from pathlib import Path
from RepoManager import RepoManager
from AliasManager import AliasManager

GUT_DIRECTORY = ".gut"


def repo():
    # TODO: fix to also open other directories or paths.
    RepoManager.open_repo()


def run(args):
    return subprocess.run(args, capture_output=True).stdout.decode('UTF-8')


# Configure the current repo as a gut repo.
def config():
    RepoManager.config_current_dir()


def aliases():
    print("GutRepo Aliases:")
    for alias in AliasManager.get_alias_keys():
        print(" - %s" % alias)


def main():
    # Create metadata ~/.gut directory if it doesn't exist
    home_path = str(Path.home())

    # Ensure .gut directory exists
    dir_path = Path("%s/%s" % (home_path, GUT_DIRECTORY))
    if not dir_path.is_dir():
        dir_path.mkdir()

    # Ensure metadata files exist
    RepoManager.ensure_file_exists()
    AliasManager.ensure_file_exists()

    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--aliases", nargs='*', help="Show all aliases.")
    parser.add_argument("-c", "--configure", nargs='*', help="Instantiates this the current directory as a gut repo.")
    parser.add_argument("-r", "--repo", nargs='*', help="Opens the github repository associated with this repository, "
                                                        "or file if specified.")
    args = parser.parse_args()
    print("args: " + str(args))
    if args.configure is not None:
        config()
    elif args.repo is not None:
        repo()
    elif args.aliases is not None:
        aliases()

    # TODO: Create a delete gut repo
    # TODO: Show all aliases
    # TODO: Prevent alias collision
    # TODO: open directory within github repo
    # TODO: open file within github repo


if __name__ == "__main__":
    main()
