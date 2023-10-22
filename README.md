# cli-compass
## This project is unofficial and won't support all schools using Compass
### We will not be responsible for any bans/data leaks/damage/trouble/etc. caused by this project
### You have been warned and you use this client at your own risk!


## About

This is an unofficial command line based Compass Education client, that uses reverse-engineered API calls to retreive various pieces of information.

Since this client is just text-based, it loads significantly faster than the official client without all of the extra visuals

## Installation

To install run the following commands:

``` shell
    # clone the repo
    $ git clone https://github.com/cornflowerenderman/cli-compass.git

    # change the working directory to compass cli
    $ cd cli-compass

    # install the requirements
    $ python3 -m pip install -r requirements.txt

    # execute program
    $ python3 getSchedule.py
```

## Command line options
```
Features can be enabled or disabled by using different command line switches:
    --help:                 Shows help page
    --show-learning-tasks:  Shows learning tasks (not implemented, time expensive)
    --show-chronicles:      Shows chronicles (not implemented)
    --show-events:          Shows events (not implemented)
    --nerd:                 Shows extra information that is useless to the average user
    --no-schedule:          Disables schedule
    --no-attendance:        Disables attendance
    --no-auth-test:         Disables testing if valid login (not recommended)
    --no-user-id:           Disables finding user-id (will break stuff, don't use)
    --show-news:            Enables news (semi time expensive)
    --news-max n:           Sets max news entries (can sometimes increase speed)
    --no-fancy-links:       Disables web-style links (Use if not supported by your terminal)
```
## TODO
    
    -  Better exception handling (mostly complete)
    -  Add learning tasks being shown on schedule
    -  Add events & chronicle entries
    -  Add License
    -  More goals?

## Contributions
Pull requests and issues are welcomed, as they can help us to improve this client and fix bugs

If you want to contact me personally (Eg. you are part of Compass and want me to take down this code), contact me here: cornflowerenderman _*at*_ duck.com

