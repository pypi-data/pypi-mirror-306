## Waldur Site Agent TUI
Waldur Site Agent TUI is a terminal user interface (TUI) for Waldur Site Agent.

## How to use
### Installing
- Install Poetry https://python-poetry.org/docs/#installing-with-pipx
- In the cloned project install Poetry dependencies with ```poetry install```
- Run the TUI with ```poetry run python src/main.py```
### UI
- To switch between TUI elements
  - Press ‘tab’
- To switch to a different tab
  - Select the tab switcher
  - Press ‘left arrow’ or ‘right arrow’ to switch tabs



## Release notes
### Release notes 0.1.0
- Added dashboard tab
  - Only includes static test info for now
- Added logs tab
  - Includes 3 log categories
  - Logs are searchable
  - UI for search by date is added
    - Not yet functional
  - A simple export logs button
    - Export logs that can be viewed
    - May need to change the functionality in the future
  - Table for log info
    - Only includes test logs for now
- Added configured offerings tab
  - Offerings are searchable
  - A list view for available offerings
  - Each offering has a view for its included items and values
  - Only includes test info for now
- Added keybindings
  - ‘q’ for quitting the TUI
  - ‘e’ for a simulated error popup
- Know Bugs
  - None
