# PongClone

A simple clone program of the original 1972 Atari game Pong written and coded in Python with Jupyter Notebook. Requires Python 3.14 and is managed with [uv](https://docs.astral.sh/uv/).

Currently makes use of the 'turtle', 'random' and 'os' Python modules.

Can be played single player, with 2 people or let the computer face itself.

There are 2 AI modes so far:
  The first 'cheats' in that it knows where the ball is at all time, much like a human player does with their eyes.
  The second predicts where the ball will be given its trajectory and possible bounces.


Also has a secondary 'Advanced' mode where the paddles may also move left and right.

# Running Locally

    cd src && uv run Pong_Clone.py

# Docker Command Line Startup Sequence

    docker buildx build --load -t pongclone .
    docker run -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/snd --privileged=true pongclone

# Testing
