import subprocess
from pathlib import Path
import re

from AliasManager import AliasManager

GUT_DIRECTORY = ".gut"
REPO_FILE = "repos"
GH_HTTP_PATTERN = 'https://github.com/(.*)/(.*)'
GH_GIT_PATTERN = 'git@github.com:(.*)/(.*)'
GH_HTTP_TEMPLATE = "https://github.com/%s"
BRACKET_PATTERN = "\[.*?\]"


class RepoManager:

    @staticmethod
    def config_current_dir():
        path = run(["pwd"]).strip()
        user = None
        repo = None
        config_path = Path("./.git/config")
        if config_path.is_file():
            user = get_remote_origin_user_repo(config_path.read_text())[0]
            repo = get_remote_origin_user_repo(config_path.read_text())[1]

        repo_properties = RepoManager.extract_repo_properties(path)
        original_alias = repo_properties["alias"] if "alias" in repo_properties.keys() else None

        alias = str(input("Repo Alias [%s]: " % original_alias))
        if alias:
            if not alias == original_alias:
                AliasManager.delete_by_name(original_alias)
                alias_entry = AliasManager.craft_alias(alias, path)
                AliasManager.add_alias(alias_entry)
        else:
            alias = original_alias

        print("Path [%s]: auto" % path)
        print("GitHub User [%s]: auto" % user)
        print("GitHub Repo [%s]: auto" % repo)

        repo_entry = ["[%s]\n" % path, "alias = %s\n" % alias, "user = %s\n" % user, "repo = %s\n" % repo]
        RepoManager.append_repo_lines(repo_entry)

    @staticmethod
    def extract_repo_properties(repo_path):
        properties = {}
        maintained_lines = []
        with open(get_repo_file_path(), 'r') as file:
            path_found = False
            for line in file.readlines():
                if path_found:
                    if re.match(BRACKET_PATTERN, line.strip()) is not None:
                        path_found = False
                        maintained_lines.append(line)
                    else:
                        key_val = line.strip().split(" = ")
                        properties[key_val[0]] = None if key_val[1] == "None" else key_val[1]
                else:
                    if "[%s]" % repo_path in line:
                        path_found = True
                        properties["path"] = line.strip("\n[]")
                    else:
                        maintained_lines.append(line)
            file.close()

        RepoManager.write_repo_lines(maintained_lines)

        return properties

    @staticmethod
    def read_properties(repo_path):
        properties = {}
        with open(get_repo_file_path(), 'r') as file:
            path_found = False
            for line in file.readlines():
                if path_found:
                    if re.match(BRACKET_PATTERN, line) is not None:
                        path_found = False
                    else:
                        key_val = line.strip().split(" = ")
                        properties[key_val[0]] = None if key_val[1] == "None" else key_val[1]

                else:
                    if "[%s]" % repo_path in line:
                        path_found = True
                        properties["path"] = line.strip("\n[]")
            file.close()
        return properties

    @staticmethod
    def write_repo_lines(lines):
        with open(get_repo_file_path(), 'w') as file:
            for line in lines:
                file.write(line)
            file.close()

    @staticmethod
    def read_repo_lines():
        return open(get_repo_file_path(), 'r').readlines()

    @staticmethod
    def append_repo_lines(new_lines):
        maintained_lines = new_lines
        with open(get_repo_file_path(), 'r') as file:
            maintained_lines.extend(file.readlines())
            file.close()

        with open(get_repo_file_path(), 'w') as file:
            for line in maintained_lines:
                file.write(line)
            file.close()

    @staticmethod
    def ensure_file_exists():
        repo_file_path = Path("%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPO_FILE))
        if not repo_file_path.is_file():
            repo_file_path.touch()

    @staticmethod
    def open_repo():
        path = run(["pwd"]).strip()
        repo_path = find_parent_repo_path(path)
        if repo_path is not None:
            repo_properties = RepoManager.read_properties(repo_path)
            url = construct_base_url(path, repo_properties)
            if url:
                print("Opening '%s'..." % url)
                if subprocess.run(["open", url], capture_output=True).returncode == 1:
                    print("Failed to open '%s'" % url)
            else:
                print("No git origin found.")
                print("Please add a remote repository: `git remote add origin https://github.com/user/repo.git`")
        else:
            print("No parent gut repo found.")


def find_parent_repo_path(path):
    for line in RepoManager.read_repo_lines():
        stripped_line = line.strip()
        if re.match(BRACKET_PATTERN, stripped_line) is not None:
            repo_path = stripped_line.strip("[]")
            if repo_path in path:
                return repo_path
    return None





def construct_base_url(path, repo_properties):
    keys = ["user", "repo"]
    for key in keys:
        if key is None or key not in repo_properties.keys():
            return None
    user = repo_properties[keys[0]]
    repo = repo_properties[keys[1]]
    if user is None or repo is None:
        return None

    path_parts = path.split(repo_properties["path"])
    path_suffix = path_parts[1].strip('/')

    url = GH_HTTP_TEMPLATE % user
    suffix_path_elements = [repo.replace(".git", "")]

    if path_suffix:
        path_type = "tree" if Path(path).is_dir() else "blob"
        branch = get_current_branch()
        suffix_path_elements.extend([path_type, branch, path_suffix])

    return "%s/%s" % (url, "/".join(suffix_path_elements))


def get_remote_origin_user_repo(config_text):
    for pattern in [GH_HTTP_PATTERN, GH_GIT_PATTERN]:
        search_result = re.search(pattern, config_text)
        if search_result is not None:
            return search_result.groups()
    return None


def run(args):
    return subprocess.run(args, capture_output=True).stdout.decode('UTF-8')


def get_repo_file_path():
    return "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, REPO_FILE)


def get_current_branch():
    return run("git rev-parse --abbrev-ref HEAD".split(' ')).strip()
