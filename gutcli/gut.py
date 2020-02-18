import argparse
import subprocess
from gutcli.GutRepo import GutRepo
from gutcli.AliasManager import AliasManager


def repo():
    GutRepo().open_remote_url()


def run(args):
    return subprocess.run(args, capture_output=True)


# Configure the current repo as a gut repo.
def config():
    gutrepo = GutRepo()
    gutrepo.purge()
    gutrepo.configure()
    gutrepo.save()


def aliases():
    print("GutRepo Aliases:")
    for alias in AliasManager.get_alias_keys():
        print(" - %s" % alias)


def main():
    # Create metadata ~/.gut directory if it doesn't exist
    GutRepo.ensure_metadata_dir_exists()

    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configure", nargs='*', help="Instantiates this the current directory as a gut repo.")
    parser.add_argument("-r", "--repo", nargs='*',
                        help="Opens the github repository associated with this repository, or file if specified.")
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
