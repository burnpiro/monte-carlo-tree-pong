# monte-carlo-tree-game
Monte Carlo Tree Search for pong game

### Requirements
```bash
python=>3.7
gym==0.16.0
```

## Nim Game

### Usage
To start the game
```bash
python nim_runner.py
```

Setup a game (3 piles and 20 randomly set objects):
```bash
Set game settings (`number of piles` `number of objects`): 3 20
```

Making a move (remove 2 objects from second pile):
```bash
Your move: 1 2
```

## Pong game

Start random game
```bash
python run_gym_random.py
```

Start responsive game
```bash
python run_gym_keyboard.py
```

Read the instructions in the console.

### Implementation notes

`gym.make` returns environment (`env`) which allows us to make steps by passing action as a parameter to `env.step(action)`.

`env.step()` returns Tuple with 3 values:
- **object** - memory dump 210 x 160 x 3 flatten to 10800
- **reward** - -1.0, 0, 1.0 (loss, neutral, win)
- **done** - is game done

We can close and restore states by using one of those methods:

- **clone_state()** - close emulator state w/o system state (not cloning pseudorandomness)
- **restore_state(state)** - restores state from **close_state**
- **clone_full_state()** - close emulator with system state
- **restore_full_state(state)** - restores state from **clone_full_state**

#####Usage:
```python
state = env.clone_state()
```