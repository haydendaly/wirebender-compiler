# Compiler for Wire Bender Language

## Usage

```sh
$ python3 main.py -f /input/script.wire
```

Will output compiled `/output/script.wirec`

## Example Program

The language includes recursion by adopting a Lisp syntax.

```
(var num_times 4)
(var bend_angle (/ 360 num_times))

(repeat num_times (
    (feed 2)
    (bend bend_angle)
))

(rotate 90)

(feed 100)
```

This compiles to the following:

```
feed 2
bend 90.0
feed 2
bend 90.0
feed 2
bend 90.0
feed 2
bend 90.0
rotate 90
feed 100
```

## Language Features

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
