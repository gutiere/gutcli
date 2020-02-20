from pathlib import Path

ALIAS_TEMPLATE = 'alias %s%s="cd %s"\n'
ALIAS_KEY_PREFIX = "gut."


class AliasManager:

    @staticmethod
    def delete_by_name(alias_name):
        lines = []
        with open(get_alias_file_path(), 'r') as file:
            for line in file.readlines():
                if not line.split('=')[0].split(' ')[1] == ALIAS_KEY_PREFIX + alias_name:
                    lines.append(line)
        file.close()
        with open(get_alias_file_path(), 'w') as file:
            for line in lines:
                file.write(line)
        file.close()

    @staticmethod
    def add_alias(alias):
        with open(get_alias_file_path(), 'a+') as file:
            file.write(alias)
        file.close()

    @staticmethod
    def craft_alias(name, path):
        return ALIAS_TEMPLATE % (ALIAS_KEY_PREFIX, name, path)

    @staticmethod
    def get_alias_keys():
        aliases = []
        with open(get_alias_file_path(), 'r') as file:
            for line in file.readlines():
                aliases.append(line.split('=')[0].split(' ')[1])
        file.close()
        return aliases


def get_alias_file_path():
    return "%s/.gut/aliases" % str(Path.home())
