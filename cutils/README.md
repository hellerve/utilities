cutils
======

This is easily the biggest subdirectory of this repo. Most
of the files are from Zed Shaws' wonderful "Learn C The Hard Way",
which is the best resource to learn C from scratch at the moment I think.

There are also a few files from a Threading book called "The Art of Concurrency
by Clay Breshears.

Finally, the file `Debug/benchmark.h` I copied from a StackOverflow answer
I cannot seem to find anymore.

Please note that even if it is called cutils, there are also C++ files in this
repo. This is due to the fact that some of the files belong to each other, also
the name cpputils does not roll of the tongue as easily.

What's included
---------------

**filestat**:

This implements a small utility that gets basic informations for a file.
Please note that it will only work on unix systems.

**find_usb**:

This implements a small utility that gets information on all USB devices that
are plugged in. It is Linux-based, you can compile it by passing the '-lusb' 
argument to the compiler(example:`gcc find_usb.c -lusb -o find_usb`).

**Directory: ConcurrentStuff**

**Concurrent Barriers/pth_barrier:**

This implements a simple barrier for threading.

**Directory: Concurrent Sorts**

**OmpOddEvenSort:**

This implements Odd-Even-Sort based on the implicit Open Message Passing
framework.

**OmpShellSort:**

This implements Shellsort based on the implicit Open Message Passing framework.

**WinBubSort:**

This implements Bubble Sort based on Windows Threads.

**Directory: MapReduce**

**FriendlyNumsMapReduce:**

This implements a search algorithm for friendly numbers based on the implicit
Open Message Passing framework.

**MapReduceSum:**

This implements summation of an array using MapReduce based on pthread.

**Directory: Debug**

**benchmark:**

This file is for getting the system time in a system-independent manner(by
calling the `get_time()` function which returns a double representing seconds.

**debugheader:**

This wonderful header contains a few macros. Explaining all of them would really
be too much pain, so I suggest reading `Debug/debugtest.c` to see an example of how
to use it.

**Directory: Hashmap**

**hashmap:**

This implements a simple hashmap.
