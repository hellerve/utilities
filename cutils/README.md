cutils
======

This is easily the biggest subdirectory of this repo. Most
of the files are from Zed Shaws' wonderful "Learn C The Hard Way",
which is the best resource to learn C from scratch at the moment I think.

There are also a few files from a Threading book called (look it up).

Finally, the file `Debug/benchmark.h` I copied from a StackOverflow answer
I cannot seem to find anymore.

What's included
---------------

**Directory: ConcurrentStuff**
Coming soon.

**Directory: Debug**

**benchmark:**

This file is for getting the system time in a system-independent manner(by
calling the `get_time()` function which returns a double representing seconds.

**debugheader:**

This wonderful header contains a few macros. Explaining all of them would really
be too much pain, so I suggest reading `Debug/debugtest.c` to see an example of how
to use it.

**Directory: Hashmap**

**hashmap**:

This implements a simple hashmap.
