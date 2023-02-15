# Compiler for Wire Bender Language

## Setup

```sh
$ virtualenv fab
$ source fab/bin/activate
$ pip install -r requirements.txt
```

## Usage

```sh
$ python3 src/main.py
```

This will take in `/input/script.wire` and output the compiled code to `/output/script.wirec`

## Example Program

The language includes recursion by adopting a Lisp syntax.

```lisp
(def polygon (sides)
    ((var bend_angle (/ 360 sides))
    (repeat sides (
        (feed 2)
        (bend bend_angle)
    )))
)

(var num_sides 5)

(polygon num_sides)

(rotate 90)

(feed 100)
```

This compiles to the following:

```
feed 2
bend 72.0
feed 2
bend 72.0
feed 2
bend 72.0
feed 2
bend 72.0
feed 2
bend 72.0
rotate 90
feed 100
```

## Language Features

### `repeat N`

Repeat the nested command `N` times. `end` must be used to end the repeat block. We `eval` out this directly and write it `N` times in the output -- we can toggle this.

### `feed N`

Feed the machine forward by `N` units.

### `bend N`

Bend the wire by `N` degrees.

### `rotate N`

Rotate the wire by `N` degrees.

### `var NAME N`

Define a variable `NAME` with value `N`.
