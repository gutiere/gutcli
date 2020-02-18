from pathlib import Path

GUT_DIRECTORY = ".gut"
ALIAS_FILE = "aliases"
ALIAS_KEY_TEMPLATE = "gut.%s"


class AliasManager:

    @staticmethod
    def delete_by_name(alias_name):
        alias_key = ALIAS_KEY_TEMPLATE % alias_name
        lines = []
        alias_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, ALIAS_FILE)
        with open(alias_file, 'r') as file:
            for line in file.readlines():
                if not line.split('=')[0].split(' ')[1] == alias_key:
                    lines.append(line)
        file.close()

        with open(alias_file, 'w') as file:
            for line in lines:
                file.write(line)
            file.close();

    @staticmethod
    def add_alias(alias):
        alias_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, ALIAS_FILE)

        with open(alias_file, 'a+') as file:
            file.write(alias)
            file.close();

    @staticmethod
    def craft_alias(name, path):
        template = ALIAS_KEY_TEMPLATE
        key = ALIAS_KEY_TEMPLATE % name
        return 'alias %s="cd %s"\n' % (key, path)

    @staticmethod
    def get_alias_keys():
        aliases = []
        alias_file = "%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, ALIAS_FILE)
        with open(alias_file, 'r') as file:
            for line in file.readlines():
                aliases.append(line.split('=')[0].split(' ')[1])
        file.close()
        return aliases

    @staticmethod
    def ensure_file_exists():
        alias_file_path = Path("%s/%s/%s" % (str(Path.home()), GUT_DIRECTORY, ALIAS_FILE))
        if not alias_file_path.is_file():
            alias_file_path.touch()
            alias_file_path.write_text('alias guts="source ~/.gut/aliases"')
