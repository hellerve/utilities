utilties
======

This repository contains various Javascript utilities, mostly from the 
book "JavaScript Patterns" by Stojan Stefanov and "Eloquent Javascript" 
of Marijn Haverbeke. The algorithms were partially updated, but the 
idea behind them stays the same.

Most of them are implementations of features of other programming
languages, such as mixins and classes, but also constants and a validator
that is best explained through the accompanying test file `validatortest.js`.

It is not the only repository out there that contains those patterns,
but my rewritten version are for private purposes anyway.

Also it includes many Python utilities, such as decorators, metaclasses,
descriptors and many other things to customize (and even break) your Python.

What's included
---------------

The Python code is documented pretty okay, so I will not explain it too verbosely
here:

**decorators**:

All kinds of decorator utilities.

**breaking_python**:

All you need to make python a typechecking language that can import XML(by generating
class code from it). Do not use it. It's terrible, but way cool.

Javascript is not documented too well, so the explanations for them are a bit lengthy.

**classical:**

This implements class-centric(so OO) utilities, such as an `inherit()` function
that lets a given child inherit from a given parent.

You can also find a functiont here that creates new instances of 'classes' - if
you will -, with an optional parent argument which exploits virtual inheritance.

**constant:**

This implements a namespace-like room for constants in Javascript. Note that
those are *not really* constant, just 'hard to reach'.

**construct:**

This implements the Sandbox pattern is maybe the most famous - and most 
misunderstood, as I learned from Google - pattern in the book. It is a 
constructor - as my name implies -, but we hand over a callback, so it
can be executed in its' namespace and use modules that are part of it.

**extend:**

Extends an object with the properties of another supplied object.
Note that this is not a deep copy; this is what `extendDeep()` is for.
There is also a function called `mixin` in there that creates a new 
object from the properties of various objects, just like the mixins from
e.g. Ruby.

**handler:**

A very simple example that takes a callback fucntion which might
yield an event and sets up an environment for you to execute said
callback in.

**higherorder:**

This is the "Haverbeke file". It implements a few bascis from functional
programming, such as `map()`, `reduce()` and utilities like `negation()`,
which negates a given function and `forEach()` my favourite loop construct.

**validator**:

I find it hard to explain this one. Basically, it checks input(json) for 
given structures and reports whether it meets the criteria. The best 
documentation is the example that is included, I guess.
