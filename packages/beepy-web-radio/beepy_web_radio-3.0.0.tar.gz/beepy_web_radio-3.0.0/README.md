# Beepy Web Radio

## Overview

This is a Beepy app to play web radio, powered by [radio.garden](http://radio.garden). The application is written in Python, using [Textual](https://textual.textualize.io/) for the TUI. You should install this through the [bapp-store](https://github.com/conor-f/bapp-store), but if you want to run this on a non-Beepy device, the `justfile` gives a pretty clear indication of what to do (or look at the Developer Quickstart below). In addition to the TUI, you can use `beepy-web-radio` as a regular CLI.


![Demo GIF](https://private-user-images.githubusercontent.com/2671067/377930795-ec0ee36a-c2f8-41ce-ab58-c6c1ca76e409.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjkyNjY0OTUsIm5iZiI6MTcyOTI2NjE5NSwicGF0aCI6Ii8yNjcxMDY3LzM3NzkzMDc5NS1lYzBlZTM2YS1jMmY4LTQxY2UtYWI1OC1jNmMxY2E3NmU0MDkuZ2lmP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MTAxOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDEwMThUMTU0MzE1WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NDgzM2UxYmI4ZGEzYTdhNjkxYjljOTlhMDNkYWViMWQ5YjNjYWY1NThiYjZhN2ZlMWRlZTg5M2JkMjlhZmJhNyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.H17GFtEHNxbghkp6_o1R95H4cu-sXoJMDUaeatoFwiM)


```
$ beepy_web_radio --help
usage: beepy_web_radio [-h] {search,play,stop} ...

Beepy Web Radio CLI

positional arguments:
  {search,play,stop}  Available commands
    search            Search for stations
    play              Play a station
    stop              Stop playback

options:
  -h, --help          show this help message and exit
```

## Developer Quickstart

```
$ just init
$ just run
$ just run
$ just run --help
```

The `just init` rule will install a number of pre-commit hooks in addition to installing the actual project.
