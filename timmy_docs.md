# Timmy Docs

## Todos

- [ ] TODO: better Timmy sprite
- [ ] TODO: better collision detection, or at least better bounding boxes.
- [ ] TODO: scrolling text about box screen
- [ ] TODO: Make sure we have all the attributions in the about box credits.
- [ ] TODO: write a README to distribute with the game, with also credits and attributions and instructions.
- [ ] TODO: add a page on rastercat.com to promote the game(need to cleanup the other stuff on the site too).
- [ ] TODO: share on itch.io
- [ ] OPTIONAL: add falling glow worm mobs.
- [ ] OPTIONAL: add different color bats that you have to shoot twice to die for harder levels.
- [ ] OPTIONAL: add a rat mob boss that spits venom at you.
- [ ] 

## Overview

**Timmy, Cave Explorer** is a space invaders style game set in a cave with a lost boy as its hero

## Story

Timmy is trapped in a cave! He was exploring near his grandparents’ farm and discovered a cave, but now he is lost inside, and things are getting pretty weird. Strange, glow-in-the-dark fungi is growing in the cave, so he can see.

There are strange, aggressive bats. Fortunately, Tim, brought along his pellet pistol so he can defend himself. The bats are dropping “things” down at him. There also  may be other strange creatures attacking from above.

Help Timmy defend himself!

## Technical Details

The space invaders game we are basing this off of is a version of the same one we used for our coding class on Raspberry Pi and Python. This time we’re starting with their version two that ads scoring, lives, sound, and levels.

It uses PyGame-Zero which is a game development library for Python, meant for Rapsberry Pi, but which also works on other computers.

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

- Rocks (pelets, base) https://opengameart.org/content/a-bunch-of-rocks 

- - We replaced these.

- Pistol: https://opengameart.org/content/flintlock-pistol 

  - If we redraw Timmy sprite again remove this.

- Blood: https://opengameart.org/content/pixelated-blood-animations

- Spider: https://opengameart.org/content/lpc-spider 

- Music: https://opengameart.org/content/mystical-caverns 

* Cave Tileset: https://opengameart.org/content/cave-tileset-0



