# ZeroPython

## Rules

Develop code with Python programming language, without following features:

- `import`,
- `from` `import`,
- defining functions with builtin names,
- calls of builtin functions except [`int`, `list`, `dict`, `bool`, `str`, `float`, `tuple`, `type`],
- calls of methods (eg. `my_list.append()`),
- `try` clauses,
- `break` and `continue` statements,
- names (variables or functions) with builtin names or trailing underscore (eg. `my_var_`),
- `for` loop,
- list comprehensions,
- dict comprehensions,
- set comprehensions,
- generator expressions,
- `yield` and `yield from` statements,
- `raise` statements,
- `assert` statements,
- `else` statements of `while` loop,
- `global` statements,
- `nonlocal` statements,
- following operators on list: [`+`, `+=`, `==`, `>=`, `<=`, `>`, `<`, `!=`, `*=`],
- 3 arg form of `type`,
- class definitions,
- `in` and `not in` operator,
- `is` and `is not` operator,
- positional only arguments, keyword only arguments, keywords defaults arguments, defaults arguments, variadic arguments, variadic keyword arguments,
- slices,
- packing, unpacking

## Setup

### Install

```bash
pip install zeropython
```

## Exercises proposals

### append

return a list with the item added at the end of the given list

input: `[1, 2, 3]`

output: `[1, 2, 3, 4]`

### extend

return a list concatenated from the 2 given lists

input: `[1, 2, 3], [3, 4]`

output: `[1, 2, 3, 3, 4]`

### clear

return a cleared list

input: `[1, 2, 3]`

output: `[]`

### sort

return `None` and sort the given list

input: `[3, 1, 2]`

output: `[1, 2, 3]`
