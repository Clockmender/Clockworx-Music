# Clockworx-Music

### This version now loads Pip and PyGame automatically.

This software suite is a Blender Add-on designed to work with Blender Version 2.9x and higher.

<img width="158" alt="Screenshot 2021-05-28 at 13 04 45" src="https://user-images.githubusercontent.com/29657804/119981231-4a367200-bfb5-11eb-893d-f9dd6bc4bd3e.png">

https://www.blender.org

![Main Image 1](https://github.com/Clockmender/Clockworx-Music/blob/master/images/cm-3.png)

A set of Nodes and New Node Editor to produce Music from Animations and Animations from Music, with Live! MIDI control included.

Very much a WIP for now, some experimental code that will need making into a fully compliant Blender Add-on.

The idea is to be able to produce animations from MIDI files, sounds from MIDI files and Procedural Sounds to load into VSE to make sound tracks to animations. It will also feature some low level DAW functions to allow the production of music from a Pianoroll.

This has been developed from earlier Animation Nodes additional nodes, but now using its own Node Editor.

More work needs to be done, so please don't use this for production until a release has been made and all test and first stage development have been completed.

![Main Image 2](https://github.com/Clockmender/Clockworx-Music/blob/master/images/cm-1.png)

![Main Image 3](https://github.com/Clockmender/Clockworx-Music/blob/master/images/cm-2.png)

Contact me via the Issues page with any questions, or suggestions.

## Installation:

Download the Repo.

Zip up the **Clockworx-Music** folder.

Install like any other Blender Add-on from User Preferences.

## Pygame

At some stage this will be required for Live MIDI & Sound connections.

You should make sure pip is installed by navigating to the blender python/bin directory then:

./python3.7m -m ensurepip

For Blender 2.93:

./python3.9 -m ensurepip

Then install the libraries (I think Windows might be python3.7m.exe)

./python3.7m -m pip install pygame

For Blender 2.93:

./python3.9 -m pip install pygame

### Make sure you use the ./ infront of the python, or you will not use the local Blender Python

### SoundDevice is not required with Clockworx Music Nodes.
