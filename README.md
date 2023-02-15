# Compiler for Wire Bender Language

## Usage

```sh
$ python3 main.py -f /input/script.wire
```

Will output compiled `/output/script.wirec`

## Commands

### `repeat N`

Repeat the nested command `N` times. `end` must be used to end the repeat block.

### `feed N`

Feed the machine forward by `N` units.

### `bend N`

Bend the wire by `N` degrees.

### `rotate N`

Rotate the wire by `N` degrees.

### `var NAME N`

Define a variable `NAME` with value `N`.

## Example Script

```
feed 10
var num_rotations

repeat num_rotations
    feed 2
    bend 3.6
end

rotate 90

feed 100
```
