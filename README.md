# closure-language

Tentatively called "**SussLang**". An implementation of a closure-based programming language I programmed a while back in Python.

# 👉 [Run it Online at REPL.it!](https://repl.it/@Inothernews1/Jonah-Language) 👈

# 💻 How to Run Locally

You must have Python 3 installed.

1. Clone the repository, `git clone https://github.com/JonahSussman/closure-language.git`
2. Open the folder, `cd closure-language`
3. Run `Python3 main.py` to launch the REPL

You can either use the REPL by hitting enter, or load a script from the `src` directory by typing in its filename.

The contents of `src` are as follows:

| Filename        | Description                                                |
|-----------------|------------------------------------------------------------|
| `_rand`         | A random number generator. Call it like `rand()`.          |
| `_vector`       | A simple 2D vector object. Supports adding and length.     |
| `_list`         | A linked list implementation. Use this in place of arrays. |
| `diamond.suss`  | Prints a diamond of a given size.                          |
| `fib.suss`      | Prints all fibonacci numbers lower than a given number.    |
| `fizz.suss`     | Fizzbuzz!                                                  |
| `guess.suss`    | The computer has a number, and you have to guess it.       |
| `listdemo.suss` | Demo for the `_list` library.                              |
| `memory.suss`   | A memory helper / study tool.                              |
| `primes.suss`   | Prints all primes lower than a given number                |

# 💡 Language Primer

This language was an experiment in how to implement a scripting language. As such, there are many design features that I would change for the future. (`~` meaning the boolean not as opposed to the bitwise complement to name one). The core of the language is written in Python 3. A pretty slow language to implement *another* language in, but it was sufficient for my goals. 

Note that the code snippets below use **Rust syntax highlighting**. It's better than just bare code blocks, but it's not perfect.

## 🌎 Importing Other Scripts

If you want to import someone else's code, simply type `import <filename>`. Be careful, as the way this works is kind of hacky: it **unconditionally** runs the contents of the other file. This can lead to **infinite loops** if you are not careful.

## ➗ Variables

With that out of the way, let's move on to variables. SussLang's type characteristics and behaviors are extremely python-esque. There are 3 basic data types: nil, numbers and strings. To declare a variable, use the `let` statement

```rust
# Comments are defined with a pound sign at the beginning of a line
let x = 0
let s = 'I'm a string!'
let n = nil # This defines 'n' to be nil, corresponding to Python's None type.
```

To cast from a string to an integer (or a `num` type) use:

```rust
let s = '100'
let x = s -> num
```

You can also easily add, multiply and do a wide variety of other operations on variables too:

```rust
let x = 0

x = x + 1
x = x - 1
x = x * 1
x = x / 1
x = ln x
x = log x
x = sqrt x
x = 3 _root x # Nth root of x
```

## 🦜 Input & Output

The tokens `input` and `print` correspond to taking input from `stdin` and outputting to `stdout` respectively.

```rust
let x = input 'Gimme a number. '
let y = x -> num
y = y + 1
print (y -> str) + ' is bigger!'
```

## ✅ Boolean Expressions

SussLang supports a wide variety of common boolean expressions:

```rust
let x = true
let y = false

~x      # NOT x, I wish I chose a different symbol for this one
x and y
x or y
x == y
x != y
x <= y
x >= y
x < y
x > y
```

## 🌊 Control Flow

The statements in this language are pretty C-like. We have the if statement:

```rust
if (stmt) {
  ...
}
```

and the while loop:

```rust
while (stmt) {
  ...
}
```

For loops can be accomplished the old-fashioned way:

```rust
# Prints the numbers 0 to 9
let i = 0
while (i < 10) {
  print i 
  i += 1
}
```

## 🚂 Functions & Closures

The real power of SussLang comes from the way we can use functions.

We can define a function like so:

```rust
fn function(arg0, arg1) {
  let x = arg0

  return arg0
}

print function(1, 2) # Will print '1'
```

In fact, we can define functions *inside* functions. Not only that, but we can also return *the functions themselves*

```rust
fn outside() {
  fn inside() {
    print '5'
  }

  inside()

  return inside
}

let x = outside() # will print 5
x() # will print 5 again!
```

An interesting and powerful feature of this language is that the environment inside the function is *not* destroyed after calling the function. This allows us to do Object Oriented Programming believe it or not! 

```rust
fn Object(x) { # Arguments are still in scope
  let y = 'Hello world!'

  fn attr() {
    if (id == 'x') return x # return copy of x
    if (id == 'y') return y

    if (id == 'set_x') return set_x # return the _function_ set_x
    if (id == 'set_y') return set_y # which still references the 'Object' environment

    return nil
  }

  fn set_x(new_x) {
    x = new_x
  }

  fn set_y(new_y) {
    y = new_y
  }

  return attr
}

let o = Object(1)
print o('x') # prints 1
print o('y') # prints 'Hello world!'
o('set_x')(10)
print o('x') # prints 10
```

Poke around the example files in the `src` directory for more. The underscored files are of particular interest. Since the language doesn't support arrays (!!!) the default way of storing things is in a linked list, found in `_list`.

# 📜 Licence

This software is released under the MIT License. See the [LICENSE.md](LICENSE.md) file for more information.