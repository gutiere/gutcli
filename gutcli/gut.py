import argparse
import subprocess
from pathlib import Path
from gutcli.AliasManager import AliasManager
from gutcli.RepoManager import RepoManager

GUT_DIRECTORY = ".gut"


def construct_url(repo_properties):
    keys = ["user", "repo"]
    for key in keys:
        if key is None or key not in repo_properties.keys():
            return None
    user = repo_properties[keys[0]]
    repo = repo_properties[keys[1]]
    if user is None or repo is None:
        return None
    return "https://github.com/%s/%s" % (user, repo)


def repo():
    # TODO: fix to also open other directories or paths.
    path = run(["pwd"]).strip()
    repo_properties = RepoManager.read_properties(path)
    url = construct_url(repo_properties)
    if url:
        print("Opening '%s'..." % url)
        if subprocess.run(["open", url], capture_output=True).returncode == 1:
            print("Failed to open '%s'" % url)
    else:
        print("No git origin found.")
        print("Please add a remote repository: `git remote add origin https://github.com/user/repo.git`")


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
    parser.add_argument("-c", "--configure", nargs='*', help="Instantiates this the current directory as a gut repo.")
    parser.add_argument("-r", "--repo", nargs='*', help="Opens the github repository associated with this repository, "
                                                        "or file if specified.")
    parser.add_argument("-a", "--aliases", nargs='*', help="Show all aliases.")

    args = parser.parse_args()
    # print("args: " + str(args))
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
