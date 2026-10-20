# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Pong clone built on Python's `turtle` module (Tk). The whole game is one script, `src/Pong_Clone.py`, which is an nbconvert export of `src/Pong_Clone.ipynb` (note the `# In[N]:` cell markers). The two have drifted: the `.py` plays sound on Linux with `mpg123`, the notebook still uses `aplay`. Treat `src/Pong_Clone.py` as the source of truth, since the Dockerfile runs it, and mirror changes into the notebook only if asked.

The project is managed with uv (`pyproject.toml`, `uv.lock`, `.python-version` pinned to 3.14). It has no third-party dependencies; everything is stdlib. There is no linter or test suite. `[tool.uv] python-preference = "only-managed"` is set because Homebrew's Python 3.14 lacks `_tkinter`; uv-managed builds include it.

## Running

Run from inside `src/`, because sound files (`*.mp3`) are referenced by relative path and played via shell commands (`afplay` on macOS, `mpg123` on Linux, no sound on Windows):

```
cd src && uv run Pong_Clone.py
```

On startup the game asks three `numinput` dialogs: number of players (0/1/2), game mode (0 = Classic, 1 = Advanced with horizontal paddle movement and swing strength), and AI mode (0 = Simple, 1 = Predictive). Press `p` to pause, `q` to quit.

Linux/WSL needs an X display (see `notes` for the WSL `DISPLAY` export).

## Docker / CI

The `Dockerfile` is based on `ghcr.io/astral-sh/uv:python3.14-trixie-slim` and adds alsa-utils, mpg123 and `libtk8.6` (the slim image lacks Tk's shared library, so `import tkinter` fails without it). It runs `uv sync --locked`, then runs the script from `/app/src` with `uv run`. It sets `UV_PYTHON_PREFERENCE=only-system` to override the pyproject setting and use the image's Python. Running it needs host X11 and sound passthrough:

```
docker buildx build --load -t pongclone .
docker run -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/snd --privileged=true pongclone
```

`.travis.yml` builds and pushes `$DOCKER_NAMESPACE/pongclone` in one `docker buildx build --push` step. The version is hardcoded as `0.3`, matching `pyproject.toml`. A test stage then only checks that the container starts; with no `DISPLAY` the game exits immediately, so that check currently fails.

## Architecture

All state is module-level globals (`ball`, `paddleA`, `paddleB`, `score1/2`, `pause`, `running`, `ballHit`, `numPlayers`, `gameMode`, `modeAI`, ...), mutated through `global` declarations. Top-level statements run in order: create the window, ask the menu dialogs, create turtle objects and HUD text, bind `p`/`q`, then enter a manual `while running:` loop that calls `gameWindow.update()` each frame, then sleeps to cap the loop at `FPS` (default 120). All movement and the AI counters are per frame, so `FPS` sets the game speed (`tracer(0)` disables auto-refresh).

Each unpaused frame: `playerControlsSwitch` (re-binds keys every frame based on player count/mode), `moveBall`, `borderChecking` (wall bounce, scoring, ball reset), `paddleBallCollision` (reverses `dx` scaled by swing strength, adjusts `dy` via `resultingCollisionAngle`), then the AI if fewer than two humans. `limitBallSpeed` clamps `dx`/`dy` to roughly 0.5–3.

AI controls paddle B (and paddle A too when `numPlayers == 0`) by calling the same `paddleXUp/Down/Left/Right` handlers as the keyboard. It is throttled by the `speedSAI`/`speedPAI` frame counters (acts every 26 frames). The simple AI follows the ball's current y. The predictive AI uses `predictBallMovement`, which computes the bounce-adjusted landing y into the global `ballScoreYCor` when the ball crosses center; it only works in Classic mode.

Geometry is hardcoded throughout: an 800x600 window, paddles at x = ±350 with ±50 half-height, walls at y = ±290, scoring at x = ±390, 50-px paddle steps.
