# bapp-store

This is a simple app store for Beepy applications.

It works by querying Github for repos with the topic `beepy-app`, cloning them,
installing them through a `justfile`, and providing some basic interfacing such
as searching, installing, listing, and deleting applications.


## Installation

You can install the `bapp-store` by simply running `pipx install bapp-store`.


## Dependencies

- python3
- pip
- just (Install via python -m pip install rust-just if not available on apt.)
- git


## Usage

`bapp-store` - Brings up the TUI
`bapp-store list` - List applications found on Github
`bapp-store search <name>` - Searches for a Beepy app on Github
`bapp-store install <name>` - Install a Beepy app from Github
`bapp-store list-installed` - List installed applications
`bapp-store remove <name>` - Removes the Beepy app from your device


## Future Work

- There should be some concept of app versioning and pinning/installing particular
versions.
- Major refactor!
- More defensive code for directories already existing and tidying up on failures
- Limit the screen output size
