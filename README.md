Raspberry Pi - PiPy Media Kiosk Development

Goals

The original goals for this project were

a)	To produce some kind of automatic PowerPoint player, with additional features
b)	To teach myself more about Python Programming.

Further, I wanted to experiment with building the simplest kind of input device/keyboard which could be used to drive an on-screen menu. This would mean that you could have a tiny media player in the form of a Raspberry Pi Zero (or Zero-W) with no other hardware needed. It had to work without being Wi-Fi connected, however. 

Possible Uses

The main use will be for “digital signage” –  but I had thought it could be used in shops or for simple interactive slideshows in museum type displays (and you might wire up your own switches rather than use my solution, described below).

It is, at a most basic level, a simple media player, but will play powerpoint files too! So, I decided to develop a Python Programme which

1)	Had a simple, flexible re-usable menu system
2)	Would read GPIO inputs so that simple key-switches could be used as the cheapest possible keyboard.
3)	It would copy all files from a USB stick onto its own card.

It had to be able to play videos and also display images. It had to be able to do this automatically or interactively.

All the required information is in this Blog Post I made:

http://halfin-halfout.blogspot.co.uk/2017/03/pipy-media-kiosk-development.html
