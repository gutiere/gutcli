# Gut-CLI

*Github repo discovery and management.*

---

The primary benefits of using `gutcli` are:
- Consistent aliases to navigate to a Github directory, regardless of the path on each team member's machine.
- Quick access to a project's Github repo in your browser.

## Features
| Feature | Command | Description |
| --- | --- | :--- |
| GutRepo Alias | `$ gut.playground` | List all GutRepo aliases. |
| Open Github Repo | `$ gut -r` | Opens the Github repo link in your browser of the GutRepo configured in your current directory.|
| GutRepo Configuration | `$ gut -c` | Configure the current directory as a GutRepo. This **must** be a Github repo directory.|
| Auto Configuration | `$ gut --auto-configure` | This command will discovery Github repos within the current directory up to 5 layers deep and configure a GutRepo. |


## Installation
### Install
`$ pip install gutcli`
### Upgrade
`$ pip install --upgrade gutcli`


## FAQs
### What is a GutRepo?
GutRepos are the resource created for a Github repository within the `gutcli` ecosystem to manage metadata including the alias.
