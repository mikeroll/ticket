# Ticket

### What?
A little cli tool to keep your JIRA issues really simple and organized.

### Installation
```python
pip install https://github.com/mikeroll/ticket/archive/master.zip
```
... or maybe some other way.

### Configuration
You'll need a `config.yml` file in your user's config directory, that is:

- `/home/YOU/.config/ticket` in Linux
- `/Users/YOU/Library/Application Support/ticket` in OSX
- `C:\\Users\\YOU\\AppData\\Local\\mikeroll\\ticket` in Windows

See the included [example config](example_config.yml) for reference.

### Usage
This is built using the awesome [Click](https://github.com/pallets/click) library. So just stick a `--help` wherever you want and you'll be fine.

### I got 99 tickets but no sh*t ain't done
```
$ ticket show
TP-11  Open  Need to do a bunch of stuff
TP-10  Open  Need to do that
TP-9   Open  Need to do this

$ ticket new 'Someone found a bug' 'On my way!'
TP-12 | Open | 0.0h | Someone found a bug
https://jira.devops.mnscorp.net/browse/TP-12

On my way!

$ ticket start 12  # TP-12 will also work
TP-12 | In Progress | 0.0h | Someone found a bug

$ ticket show
TP-12  In Progress  Someone found a bug
TP-11  Open         Need to do a bunch of stuff
TP-10  Open         Need to do that
TP-9   Open         Need to do this

$ ticket log 12 3h
TP-12 | In Progress | 3.0h | Someone found a bug

$ ticket say 12 'Getting there'
mikeroll (mikeroll) @ 2016-05-19T16:09:50.623+0000
Getting there

$ ticket close 12 'Done!'
TP-12 | Closed | 3.0h | Someone found a bug
mikeroll (mikeroll) @ 2016-05-19T16:10:14.603+0000
Done!

$ ticket show
TP-12  In Progress  Someone found a bug
TP-11  Open         Need to do a bunch of stuff
TP-10  Open         Need to do that
TP-9   Open         Need to do this

$ ticket show 12
TP-12 | Closed | 3.0h | Someone found a bug
https://jira.devops.mnscorp.net/browse/TP-12
```

### Is it ready?
The output is not colored and the code is real ugly. Oh, and bugs, of course.
