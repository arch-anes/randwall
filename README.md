# randwall

Periodically fetch and set random wallpapers from [Wallhaven](https://wallhaven.cc/)'s toplist.

## Installation

### Standalone executable

Download the latest release from <https://github.com/arch-anes/randwall/releases>.

### Arch Linux

Install the `randwall-bin` AUR package.

### Building from source

- Clone the repo
- Create a Python virtualenv (Optional)
- Run `pip install -r requirements.txt`
- Run `python -m PyInstaller --onefile --noconsole randwall`
- A new file has been generated in the `dist` folder

## Configuration

When you start `randwall` for the first time, a configuration file with default options will be created at:

- `~/.config/randwall/config.json` on Linux
- `%AppData%\Local\randwall\randwall\config.json` on Windows
- `~/Library/Preferences/randwall/config.json` on MacOS

The configuration file contains the following settings:

- `api_key` (empty by default): This is your [Wallhaven API key](https://wallhaven.cc/settings/account). This is only needed when `purity.nsfw` is enabled.
- `max_page` (default 500): The maximum Wallhaven page to go to when fetching wallpapers (the more restrictive the keywords are, the lower this number should be set to).
- `keep` (default 10): The maximum number of wallpapers to keep in temporary folder. A value of `0` means keeping everything.
- `interval` (default 30): Fetch interval in seconds.
- `categories` (all enabled by default): These are the [Wallhaven categories](https://wallhaven.cc/toplist).
- `purity` (`sfw` only enabled by default): These are the [Wallhaven purity settings](https://wallhaven.cc/toplist). `nsfw` needs an API key.
- `include` (empty list by default): A list of keywords to use when searching for wallpapers. This is empty by default to get all keywords.
- `exclude`: A list of keywords to exclude when searching for wallpapers. By default it contains a few entries.

## Running

### Standalone executable

Simply start the executable.

### Arch Linux

Run `systemctl enable --now --user randwall`.
