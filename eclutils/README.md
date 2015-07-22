eclutils
======

This subdirectory contains utilities for Eclipse/CSP-flavoured Prolog.
They are created by myself and most likely pretty bad.

What's included
---------------

**util**:

This is the utilities module. It includes:
 * `balance/4`: takes a list of variables, their weight and a minimum and maximum position;
                tries to balance them out. Optionally takes a fifth argument of minimum distance
                between elements.
 * `absSum/2`: takes a list of values and a variable; calculates the absolute sum.
               Optionally takes a start sum.
 * `fillwith/3`: takes an element, a length and a variable; constructs a list filled with
                 element of the length given. Optionally takes an accumulator (e.g. for padding).
 * `permutation/2`: homebrew search procedure; permutes variables over a given set of things.
                    Nothing that `alldifferent/1`+`labeling/1` couldn't do, really.
