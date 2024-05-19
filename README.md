# osu-scrobbler

A lightweight program to intake osu! player status and submit the plays to last.fm.

## Requirements

- Python
- Non-Standard Python Dependencies:
  - [ossapi!](https://github.com/tybug/ossapi) - An osu!api adaptive framework for Python
- osu! & last.fm API key and secret

## Usage

System is ran entirely through command line and browser for verification. Command line intakes user information to track, browser verifies last.fm user identity. This program is written in a way that does not require the system tracking scrobbles to have the game open on the same system. Errors are written to console.
