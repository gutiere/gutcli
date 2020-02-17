import re
import os
import subprocess
from pathlib import Path
from AliasManager import AliasManager

GUT_DIRECTORY = ".gut"
REPOSITORY_FILE = "repos"
ALIAS_FILE = "aliases"
BRACKET_PATTERN = "\[.*?\]"


class GutRepo:

    def __init__(self):
        self.alias = None
        self.origin_url = None
        self.path = None

        for property in GutRepo.read_repo_md():
            # print("Init with property: " + str(property).strip())
            property_elements = property.strip().split(" = ")

            if len(property_elements) == 1:
                path = property_elements[0]
                if re.compile(BRACKET_PATTERN).match(path):
                    self.path = path.strip("[]")
            elif len(property_elements) == 2:
                key =  property_elements[0]
                value = property_elements[1]
                setattr(self, key, None if value == "None" else value)

    def get_origin_url(self):
        if not Path("./.git").is_dir():
            return None

        return run("git config remote.origin.url".split()).stdout.decode('UTF-8').strip()

    def configure(self):
        path = run(["pwd"]).stdout.decode('UTF-8').strip()
        path_dirs = path.split('/')
        current_dir = path_dirs[len(path_dirs) - 1].lower();

        try:
            alias_name = str(input("Repo Alias [%s]: " % self.alias))
            if alias_name:
                if not self.alias == alias_name:
                    AliasManager.delete_by_name(self.alias)
                    alias_entry = AliasManager.craft_alias(alias_name, path)
                    AliasManager.add_alias(alias_entry)
                    print("In order to use new aliases, run: 'source ~/.gut/aliases'")
                self.alias = alias_name
        except:
            print()
        self.path = path
        # print("Path [%s]: auto" % self.path)
        self.origin_url = self.get_origin_url()
        print("Github Origin URL [%s]: auto" % self.origin_url)

    def open_remote_url(self):
        if self.origin_url:
            print("Opening '%s'..." % self.origin_url)
            if run(["open", self.origin_url]).returncode == 1:
                print("Failed to open '%s'" % self.origin_url)
        else:
            print("No git origin found.")
            print("Please add a remote repository: `git remote add origin https://github.com/user/repo.git`")

    def purge(self):
        metadata_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPOSITORY_FILE)
        lines_to_save = []

        # Remove all old metadata lines for the current gut repo
        with open(metadata_file, 'r') as file:
            path_found = False
            for line in file.readlines():
                if path_found == True:
                    if re.compile(BRACKET_PATTERN).match(line.strip()):
                        if "[%s]" % self.path in line:
                            path_found = True
                        else:
                            lines_to_save.append(line)
                            path_found = False
                else:
                    if re.compile(BRACKET_PATTERN).match(line.strip()):
                        if "[%s]" % self.path in line:
                            path_found = True
                        else:
                            lines_to_save.append(line)
                    else:
                        lines_to_save.append(line)

        with open(metadata_file, 'w') as file:
            for line in lines_to_save:
                file.write(line)
            file.close()

    def save(self):
        metadata_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPOSITORY_FILE)
        with open(metadata_file, 'a+') as file:
            file.write(self.__str__())
            file.close()

    def __str__(self):
        string = ""
        string = string + "[%s]\n" % self.path
        string = string + "alias = %s\n" % self.alias
        string = string + "origin_url = %s\n" % self.origin_url
        return string

    @staticmethod
    def read_repo_md():
        path = run(["pwd"]).stdout.decode('UTF-8').strip()

        metadata_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPOSITORY_FILE)
        with open(metadata_file, 'r') as file:
            repo_lines = []
            repo_found = False
            for line in file.readlines():
                if re.compile(BRACKET_PATTERN).match(line.strip()):
                    if "[%s]" % path in line.strip():
                        repo_lines.append(line)
                        repo_found = True
                    elif repo_found:
                        break
                elif repo_found:
                    repo_lines.append(line)

        return repo_lines

    @staticmethod
    def ensure_metadata_dir_exists():
        home_path = str(Path.home())

        dir_path = Path("%s/%s" % (home_path, GUT_DIRECTORY))
        if not dir_path.is_dir():
            dir_path.mkdir()

        repo_file_path = Path("%s/%s/%s" % (home_path, GUT_DIRECTORY, REPOSITORY_FILE))
        if not repo_file_path.is_file():
            repo_file_path.touch()

        alias_file_path = Path("%s/%s/%s" % (home_path, GUT_DIRECTORY, ALIAS_FILE))
        if not alias_file_path.is_file():
            alias_file_path.touch()


    @staticmethod
    def cd_to_alias(alias):
        metadata_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPOSITORY_FILE)
        current_path = None
        with open(metadata_file, 'r') as file:
            for line in file.readlines():
                stripped_line = line.strip()
                if re.compile(BRACKET_PATTERN).match(stripped_line):
                    current_path = stripped_line.strip("[]")
                else:
                    key_val = stripped_line.split(' = ')
                    if key_val[0] == "alias" and key_val[1].lower() == alias.lower():
                        break
            file.close();



        if current_path == None:
            print("Alias '%s' not found." % alias)
        else:
            print("Changing directory to alias: '%s' path: '%s'" % (alias, current_path))
            os.chdir(Path(current_path))

        os.system("source ~/.gut/aliases")
        # if run(["cd", current_path]).returncode == 1:
        #     print("Failed to change directory for alias '%s'" % alias)



def run(args):
    return subprocess.run(args, capture_output=True)
