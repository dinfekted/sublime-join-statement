# Sublime JoinStatement plugin

Joins and unjoins whole statements.


### Demo

![Demo](https://raw.github.com/shagabutdinov/sublime-join-statement/master/demo/demo.gif "Demo")


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Usage

1. Unjoin statement

```
# before
hash_table = {'key1': 'val1', 'key2': 'val2'}

# after
hash_table = {
  'key1': 'val1',
  'key2': 'val2'
}

# before
condition = (a > b and b > c and c > d)

# after
condition = (
  a > b and
  b > c and
  c > d
)
```

2. Join statement

```
# before
hash_table = {
  'key1': 'val1',
  'key2': 'val2'
}

# after
hash_table = {'key1': 'val1', 'key2': 'val2'}

# before
condition = (
  a > b and
  b > c and
  c > d
)

# after
condition = (a > b and b > c and c > d)
```

You can execute command by hitting keyboard shortcut or by placing cursor and
the after opening bracket and hitting "enter" or "alt+/" (right delete). In some
cases command will not work (not a source code); if it happened you can put
space after bracket and hit enter or "right delete" to do stuff manually.

Not that it'll works only with first-level brackets. Any other nesting will be
ignored. E.g.:

```
# before
hash_table = {
  'key1': 'val1',
  'key2': {
    'subkey1': 'subval1'
  }
}

# after
hash_table = {'key1': 'val1', 'key2': {
    'subkey1': 'subval1'
  }}
```

### Commands

| Description                      | Keyboard shortcut       | Command palette                      |
|----------------------------------|-------------------------|--------------------------------------|
| Join statement                   | ctrl+alt+t              | JoinStatement: Join                  |
| Join statement (as arguments)    | [detects automatically] | JoinStatement: Join (as arguments)   |
| Unjoin statement                 | ctrl+alt+shift+t        | JoinStatement: Unjoin                |
| Unjoin statement (as arguments)  | [detects automatically] | JoinStatement: Unjoin (as arguments) |
| Join statement (after bracket)   | enter                   |                                      |
| Unjoin statement (after bracket) | alt+/                   |                                      |