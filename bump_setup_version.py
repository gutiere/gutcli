import re
from pathlib import Path

setup_file = Path("setup.py")
file_text = setup_file.read_text()
version_data = re.search(r'(\d+\.)(\d+\.)(\d+)', file_text)
old_version = "".join(version_data.groups())
new_version = old_version.replace(str(version_data.groups()[2]), str(int(version_data.groups()[2]) + 1))
file_text = file_text.replace(old_version, new_version)
setup_file.write_text(file_text)
