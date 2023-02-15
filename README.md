# Compiler for Wire Bender Language

## Commands

### `repeat N`

Repeat the nested command `N` times. `end` must be used to end the repeat block.

### `feed N`

Feed the machien forward by `N` units.

### `bend N`

Bend the wire by `N` degrees.

### `rotate N`

Rotate the wire by `N` degrees.

## Example Script

```
feed 10

repeat 100
    feed 2
    bend 3.6
end

rotate 90

feed 100
```
