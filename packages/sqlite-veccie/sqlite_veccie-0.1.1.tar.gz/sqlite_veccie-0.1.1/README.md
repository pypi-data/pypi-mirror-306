veccie: Simple SQLite Vector Distance Functions Extension
=========================================================

Veccie is a tiny sqlite extension implementing simple vector distance functions
on float32 vectors encoded in BLOBs.

Implements the following functions:

* Dot product: `dot_f32(a, b) -> a . b`
* Squared distance: `sqdist_f32(a, b) -> sum((a - b)^2)`

Where 'a' and 'b' are BLOBs containing vectors encoded as a concatenation of
32-bit IEEE floating point numbers. A native sqlite (double precision) float is
returned.


Usage
-----

### Via the `sqlite-veccie` Python library 

The `sqlite-veccie` Python package may be obtained from PyPI or built from
source (letting setuptools figure out the local compiler incantation).

The module can then be used directly with the built-in [`sqlite3`
module](https://docs.python.org/3/library/sqlite3.html), the excellent
[`apsw`](https://rogerbinns.github.io/apsw) or any other SQLite library.

    >>> import sqlite3
    >>> import sqlite_veccie
    
    >>> # Load the plugin
    >>> con = sqlite3.connect("example.db")
    >>> con.enable_load_extension(True)
    >>> con.load_extension(sqlite_veccie.path)
    
    >>> # Create a table with 100,000 random 512-dimensional vectors
    >>> import numpy as np
    >>> con.execute("CREATE TABLE example(id INTEGER PRIMARY KEY, vector BLOB NOT NULL)")
    >>> con.executemany(
    ...     "INSERT INTO example VALUES (?, ?)",
    ...     [
    ...         (id, vector.astype(np.float32).tobytes())
    ...         for id, vector in enumerate(np.random.random((100_000, 512)))
    ...     ]
    ... )
    >>> con.commit()
    
    >>> # Find the 10 vectors closest to the vector (0, 0, 0, ...)
    >>> print(
    ...     con.execute(
    ...         """
    ...             SELECT id, sqdist_f32(vector, ?) AS distance
    ...               FROM example
    ...              ORDER BY distance
    ...              LIMIT 10
    ...         """,
    ...         (np.zeros(512, dtype=np.float32).tobytes(),),
    ...     ).fetchall()
    ... )


### From source

You can [build `veccie.c` like any other SQLite
extension](https://www.sqlite.org/loadext.html#compiling_a_loadable_extension),
for example, under Linux you can use:

    $ gcc -g -fPIC -shared -O3 veccie.c -o veccie.so

You must have the `sqlite3ext.h` header in your include path.

You can also pull the ready-made binary out of the installed ``sqlite_veccie``
Python package: use `python -m sqlite_veccie` to print its filename.

Once built you can use it directly in SQLite like so:

    $ sqlite example.db
    sqlite> .load ./veccie.so
    
    sqlite> CREATE TABLE example(id INTEGER PRIMARY KEY, vector BLOB NOT NULL);
    sqlite> INSERT INTO example VALUES (0, x'0000000000000000'); -- (0.0, 0.0)
    sqlite> INSERT INTO example VALUES (1, x'0000803f0000803f'); -- (1.0, 1.0)
    sqlite> INSERT INTO example VALUES (2, x'0000004000008040'); -- (2.0, 4.0)
    
    sqlite> -- Get the distance of each vector from 1.0, 1.0
    sqlite> SELECT id, sqdist_f32(vector, x'0000803f0000803f') FROM example; 
    0|2.0
    1|0.0
    2|10.0


Why?
----

These functions happen to be the distance metrics for the embeddings used by my
[clippie](https://github.com/mossblaser/clippie/) and
[faceie](https://github.com/mossblaser/faceie) implementations of
[CLIP](https://openai.com/research/clip) and
[FaceNet](https://github.com/timesler/facenet-pytorch) respectively.

It turns out that you don't need a fancy vector database when your dataset only
consists of a few hundred thousand or million vectors: brute-force search is
shockingly fast. For exapmle, calling `dot_f32` or `sqdist_f32` on every
512-dimensional vector in a 100,000 row table only adds about 30ms(!) to the
query runtime on my laptop.

This library is another piece in the collection of parts which I'm building up
as the basis for a personal photo library program. Adding these functions makes
it possible to use SQLite to store and query both photo metadata and vector
embeddings in one robust, performant and long-lived system.


Limitations
-----------

* The functions implemented by this extension require the floats within the BLOBs
  passed to them to be in the machine's native byte order. This makes any
  database using this format non-portable between architectures with different
  byte orderings. Luckily for me, I only have little-endian machines to hand so
  this isn't a problem...

* No particular claims are made about the numerical quality of the implementation
  of these functions. Again, luckly I'm using these on fairly noisy data
  (vector embeddings) where this doesn't really matter.

* The implementation of the dot product and square distance functions is pretty
  much as simple as it gets. Most compilers will do a good job of vectorising
  this yielding pretty good performance. There is still room for improvement:
  numpy's dot product implementation is about three times faster, at least when
  run on a very large batch of vectors.

* I've not yet faffed with GitHub actions to automatically build binary wheels
  for all common platforms. (Contributions welcome...)
