import argparse
import subprocess
from pathlib import Path
from RepoManager import RepoManager
from AliasManager import AliasManager

GUT_DIRECTORY = ".gut"


def repo(args, url_only):
    RepoManager.open_repo(args, url_only)


def run(args):
    return subprocess.run(args, capture_output=True).stdout.decode('UTF-8')


# Configure the current repo as a gut repo.
def config():
    RepoManager.config_dir(str(Path.cwd()), False)


def auto_configure():
    # TODO: Short circuit at a reasonable height
    queue = [Path.cwd()]
    while queue:
        current_directory = queue.pop(0)
        # Short circuit directory navigation if this is a git repo
        if Path(str(current_directory) + "/.git").exists():
            RepoManager.config_dir(str(current_directory), True)
        else:
            for item in current_directory.glob('./*'):
                if item.is_dir() and not item.name.startswith('.'):
                    queue.append(item)


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
    parser.add_argument("--url", nargs='*', help="Print URL only, without opening in the browser.")
    parser.add_argument("--auto", nargs='*')

    args = parser.parse_args()

    if args.auto is not None:
        auto_configure()
    elif args.configure is not None:
        config()
    elif args.repo is not None:
        repo(args.repo, args.url is not None)
    elif args.aliases is not None:
        aliases()


if __name__ == "__main__":
    main()
