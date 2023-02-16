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
# Variable declaration
(var arr [2 7 1 8 2 8 1 8 2 8])
(var i (// (* (rand) (len arr)) 3))
(feed (* (get arr i) 100))

# Function declaration
(def polygon (sides) (
    (var interior_angle (/ (* (- (* 2 sides) 4) 90) sides))
    (repeat sides (
        (feed 2)
        (bend interior_angle)
    ))
))
(polygon 3)

# Simple math
(feed (* (cos (rand)) 100))
```

This compiles to the following:

```
feed 100
feed 2
bend 60.0
feed 2
bend 60.0
feed 2
bend 60.0
feed 98.10696726812708
```

## Symbols

### Primitives

One arg: `feed`, `bend`, `rotate`

### Math

Two args: `+`, `-`, `*`, `/`, `%`, `**`, `//`
One arg: `cos`, `sin`, `tan`, `acos`, `asin`, `atan`, `sqrt`, `abs`, `rand`, `log`, `log10`

```lisp
(+ 1 (cos 0))
```

### Logic

Two args: `==`, `!=`, `>`, `<`, `>=`, `<=`
One arg: `not`

#### Control Flow (wip)

Three args: `ifelse`
Two args: `repeat`

```lisp
(ifelse (== (% 20 3) 1) (
    (feed 1)
) (
    (repeat 20 (
        (feed 2)
        (bend 1)
    ))
))
```

### Variables

`var`, `get`, `set`, `len`

```lisp
(var arr [1 2 3])
(var last (- (len arr) 1))
(set arr last 4)
(feed (get arr last))
```

### Functions

`def`

```lisp
(def foo (x) (
    (feed x)
))
```
