from pathlib import Path
import gutcli.constants


HOME_PATH = str(Path.home())


# Appending alias sourcing to the end of a file if it exists
def add_alias_sourcing_to_file(name):
    path = Path("%s/%s" % (HOME_PATH, name))
    if path.exists():
        if constants.SOURCE_COMMAND not in path.read_text():
            with open(path, 'a+') as file:
                file.write("\n%s\n" % constants.SOURCE_COMMAND)
            file.close()


# Ensure .gut directory exists
dir_path = Path(constants.GUT_PATH % HOME_PATH)
if not dir_path.is_dir():
    dir_path.mkdir()

# Ensure aliases file exists
alias_file_path = Path(constants.ALIASES_FILE_PATH % HOME_PATH)
if not alias_file_path.is_file():
    alias_file_path.touch()
    with open(alias_file_path, "a+") as alias_file:
        alias_file.write('alias guts="%s"\n' % constants.SOURCE_COMMAND)
    alias_file.close()

# Ensure repos file exists
repo_file_path = Path(constants.REPOS_FILE_PATH % HOME_PATH)
if not repo_file_path.is_file():
    repo_file_path.touch()

# Add aliases sourcing to files
for file_name in constants.SOURCE_FILES:
    add_alias_sourcing_to_file(file_name)
