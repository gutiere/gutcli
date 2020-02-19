import argparse
import subprocess
from pathlib import Path
from gutcli.RepoManager import RepoManager
from gutcli.AliasManager import AliasManager

GUT_DIRECTORY = ".gut"


def repo(args, url_only):
    RepoManager.open_repo(args, url_only)


def run(args):
    return subprocess.run(args, capture_output=True).stdout.decode('UTF-8')


# Configure the current repo as a gut repo.
def config():
    RepoManager.config_dir(Path.cwd(), False)


def auto_configure():
    level_cap = 5
    queue = [Path.cwd()]
    level = 0
    level_capacity = 1
    current_level_size = 0
    next_level_capacity = 0
    while queue:
        current_directory = queue.pop(0)
        # Short circuit directory navigation if this is a git repo
        if Path(str(current_directory) + "/.git").exists():
            RepoManager.config_dir(current_directory, True)
        else:
            if level < level_cap:
                for item in current_directory.glob('./*'):
                    if item.is_dir() and not item.name.startswith('.'):
                        queue.append(item)
                        next_level_capacity += 1

        current_level_size += 1
        if current_level_size >= level_capacity:
            level += 1
            level_capacity = next_level_capacity
            next_level_capacity = 0
            current_level_size = 0



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
    parser.add_argument("--auto-configure", nargs='*')

    args = parser.parse_args()

    if args.auto_configure is not None:
        auto_configure()
    elif args.configure is not None:
        config()
    elif args.repo is not None:
        repo(args.repo, args.url is not None)
    elif args.aliases is not None:
        aliases()


if __name__ == "__main__":
    main()
