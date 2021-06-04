# songGuesser-py

A python script to play an own made song guessing game. This game is inspired by the youtube show EDDS by world wide wohnzimmer.

## Host Your Own Server

When the script is beeing executed you have the option to choose between Client and Server mode.

> Default Server Settings:
>
> IP: Intern Computer IP<br/>
> Port: 1233

You need to forward your port in order to enable other persons from different networks to join your game.

## Features

- Different Game Modes
    * Normal - _Start the song playback at 0:00_
    * Speed - _Start the song playback at the refrain to get faster rounds_
    
- Guessing Modes
    * Song Title
    * Artists
    
- Customizable
    * Song Play Duration
    * User Guessing Time
    * Win Score
    
- Other Game Options
    * Option to Play Refrain - _Play the song refrain after guessing_
    * Option to ignore Case
    * Option to ignore Order
    * Option to ignore Special Characters
    * Option to ignore Additional Words - _When enabled, everything after characters like "(" , "-" etc. is beeing removed from the song title_
    * Option to ignore Artist Features

- Automatic Updates

## Usage

Install requests with pip:

``pip install requests``

Download the newest release zip and unpack the files.

Run ``songGuesser.py`` to start the script.
