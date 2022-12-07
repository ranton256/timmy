# Timmy Docs

## Todos

- [x] TODO: scrolling text about box screen
- [x] TODO: Make sure we have all the attributions in the about box credits.
- [x] TODO: write a README to distribute with the game, with also credits and attributions and instructions.
- [ ] TODO: better Timmy sprite
- [ ] TODO: share on ranton.org
- [ ] TODO: share on itch.io
- [ ] OPTIONAL: better collision detection, or at least better bounding boxes.
- [ ] OPTIONAL: get the readme in the installer and open automatically after install somehow, or provide some way to show user where it is.
- [ ] OPTIONAL: add a page on rastercat.com to promote the game(need to cleanup the other stuff on the site too).
- [ ] OPTIONAL: add falling glow worm mobs.
- [ ] OPTIONAL: add different color bats that you have to shoot twice to die for harder levels.
- [ ] OPTIONAL: add a rat mob boss that spits venom at you.
- [ ] OPTIONAL: cleanup some of the installer hacks using https://pyinstaller.readthedocs.io/en/stable/hooks.html sys _MEIPASS and https://pythonhosted.org/PyInstaller/spec-files.html#using-data-files-from-a-module

## Overview

**Timmy, Cave Explorer** is a space invaders style game set in a cave with a lost boy as its hero

## Story

Timmy is trapped in a cave! He was exploring near his grandparents’ farm and discovered a cave, but now he is lost inside, and things are getting pretty weird. Strange, glow-in-the-dark fungi is growing in the cave, so he can see.

There are strange, aggressive bats. Fortunately, Tim, brought along his pellet pistol so he can defend himself. The bats are dropping “things” down at him. There also  may be other strange creatures attacking from above.

Help Timmy defend himself!

## Technical Details

The space invaders game we are basing this off of is a version of the same one we used for our coding class on Raspberry Pi and Python. This time we’re starting with their version two that adds scoring, lives, sound, and levels.

It uses PyGame-Zero which is a game development library for Python, meant for Raspberry Pi, but which also works on other computers.

## Installer

We used PyInstaller  to create an EXE binary for Windows out of the Timmy source code and assets.

[PyInstaller]: www.pyinstaller.org

We also had to make it conditional whether or not we import and call pgzero directly from our main source file timmy1.py.

The installer spec that tells it what to include is in the file timmy.spec.

The timmy.py source file provides the wrapper to make everything work from within the generated installer.

To create the installer run this command:

The generated .EXE file will be in the dist directory.

```
pyinstaller timmy.spec
```

Run try.bat to do that and also start the game.

We used example from this Gist github to get the installer working:

* https://gist.github.com/AnthonyBriggs/cac72989c2dd3c4aeb7475237079d2fb#file-alien-py-L22

### pgzero changes

This installer working depends on some changes to the pgzero source code.

In order for the PyInstaller to work, we have to patch the pgzero source code to load a specific font path when the default font is used because the Pygame fonts are not copied directly.

We also had to change the show_default_icon() function to comment out the existing code at    pgzero/game.py:92-95 and add 'pass' to the end.

The original game design doc and notes were in this Google Doc:

* https://docs.google.com/document/d/1dXpBpyeHoPEQ0GXQPoJSiz5EnEfOdni8oTZuP3llLOc/edit# 

## Attribution

- Bat sprites based on these: https://opengameart.org/content/bat-sprite
  - No attribution instructions, but by [bagzie](https://opengameart.org/users/bagzie) and license is OGA-By-3.0, https://opengameart.org/content/oga-by-30-faq 
  - http://static.opengameart.org/OGA-BY-3.0.txt
- ~~Rocks (pelets, base) https://opengameart.org/content/a-bunch-of-rocks~~ 
- - We replaced these.
- Pistol: https://opengameart.org/content/flintlock-pistol 
  - If we redraw Timmy sprite again remove this.
  - Copyrighted to DrzArt , but still free to use and modify , if it's used you have to gave the credit please :)
  - https://opengameart.org/users/dreazer
- Blood: https://opengameart.org/content/pixelated-blood-animations
  - Just... don't lie and say you made this... cause you didn't (haha) These are free to use, go ahead. If you got the chance though, please mention us :) Or at least leave a like on facebook /sinestesiastudio or Instagram now :p /sinestesiaguy/
  - [Sinestesia](https://opengameart.org/users/sinestesia)
- Spider: https://opengameart.org/content/lpc-spider 
  - Attribute Stephen "Redshrike" Challener as graphic artist and William.Thompsonj as contributor. If reasonable link to this page or the OGA homepage.
- Music: https://opengameart.org/content/mystical-caverns 
- Please credit MichaelTheCrow if used.
- Cave Tileset: https://opengameart.org/content/cave-tileset-0
  - Art by MrBeast. Commissioned by OpenGameArt.org (http://opengameart.org)


