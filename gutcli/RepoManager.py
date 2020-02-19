import subprocess
from pathlib import Path
import re

from gutcli.AliasManager import AliasManager

GH_HTTP_PATTERN = 'https://github.com/(.*)/(.*)'
GH_GIT_PATTERN = 'git@github.com:(.*)/(.*)'
GH_HTTP_TEMPLATE = "https://github.com/%s"
BRACKET_PATTERN = "\[.*?\]"


class RepoManager:

    @staticmethod
    def config_dir(directory, auto):
        path = str(directory)
        user = None
        repo = None
        config_path = Path(path + "/.git/config")
        if config_path.exists() and config_path.is_file():
            user_and_repo = get_remote_origin_user_repo(config_path.read_text())
            if user_and_repo is not None:
                user = user_and_repo[0]
                repo = user_and_repo[1]

        # TODO: This is DESTRUCTIVE. Get the repo properties, then once it is confirmed that we are done, replace.
        repo_properties = RepoManager.extract_repo_properties(path)
        original_alias = repo_properties["alias"] if "alias" in repo_properties.keys() else None

        if auto:
            print("Auto configuring git repo: %s" % path)
            print("Repo Alias [%s]: " % directory.name)
            alias = directory.name
        else:
            alias = str(input("Repo Alias [%s]: " % original_alias))
        print("Path [%s]: auto" % path)
        print("GitHub User [%s]: auto" % user)
        print("GitHub Repo [%s]: auto" % repo)
        if alias:
            if not alias == original_alias:
                if original_alias is not None:
                    AliasManager.delete_by_name(original_alias)
                alias_entry = AliasManager.craft_alias(alias, path)
                # TODO: Prevent alias collision
                AliasManager.add_alias(alias_entry)
        else:
            alias = original_alias
        repo_entry = ["[%s]\n" % path, "alias = %s\n" % alias, "origin_user = %s\n" % user, "origin_repo = %s\n" % repo]
        append_repo_lines(repo_entry)

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

        write_repo_lines(maintained_lines)

        return properties

    @staticmethod
    def ensure_file_exists():
        repo_file_path = Path("%s/.gut/repos" % str(Path.home()))
        if not repo_file_path.is_file():
            repo_file_path.touch()

    @staticmethod
    def open_repo(args, url_only):
        path = run(["pwd"]).strip()

        if len(args) > 0:
            if args[0] in get_ls_list():
                path = "%s/%s" % (path, args[0])
            else:
                print("The file/dir '%s' does not exist in this directory." % args[0])
                return

        repo_path = find_parent_repo_path(path)
        if repo_path is not None:
            repo_properties = read_properties(repo_path)
            url = construct_base_url(path, repo_properties)
            if url:

                if url_only:
                    print("GitHub URL: '%s'" % url)
                else:
                    print("Opening '%s'..." % url)
                    if subprocess.run(["open", url], capture_output=True).returncode == 1:
                        print("Failed to open '%s'" % url)
            else:
                print("No git origin found.")
                print("Please add a remote repository: `git remote add origin https://github.com/user/repo.git`")
        else:
            print("No parent gut repo found.")


def find_parent_repo_path(path):
    for line in read_repo_lines():
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
    return "%s/.gut/repos" % str(Path.home())


def get_current_branch():
    return run("git rev-parse --abbrev-ref HEAD".split(' ')).strip()


def append_repo_lines(new_lines):
    maintained_lines = new_lines
    with open(get_repo_file_path(), 'r') as file:
        maintained_lines.extend(file.readlines())
        file.close()

    with open(get_repo_file_path(), 'w') as file:
        for line in maintained_lines:
            file.write(line)
        file.close()


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


def write_repo_lines(lines):
    with open(get_repo_file_path(), 'w') as file:
        for line in lines:
            file.write(line)
        file.close()


def read_repo_lines():
    return open(get_repo_file_path(), 'r').readlines()


def get_ls_list():
    return run("ls -1".split(' ')).split('\n')
