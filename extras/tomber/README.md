Tomber: a Python wrapper for Tomb
=================================

Found in [extras/tomber](/extras/tomber)

Description
-----------

Tomber is a python wrapper for [Tomb](https://github.com/dyne/Tomb).
It relies on Python's subprocess module for Tomb command execution.

Please note that for future compatibility with Tomb, using subprocess
execution of the tomb script is the recommended way to wrap its
functionalities in other languages.

Tomber is still under development. Any contributions are greatly
welcomed here or on its original repository
https://github.com/reiven/tomber


Installation
----------

First of all Tomb must be installed. Refer to [INSTALL](/INSTALL.md)

Then Tomber can be installed from
[PyPi](https://pypi.python.org/pypi) using
[pip](https://pypi.python.org/pypi/pip).

Enter the following command in a terminal:

	pip install tomber

Alternatively you can install it from this source repository


Example usage
-------------
```python
from tomber import *

# dig a tomb of 20mb
tdig('test.tomb',20)

# forge a key
tforge('test.key', 'this is the passphrase for the key')

# lock the tomb
tlock('test.tomb', 'test.key', 'this is the passphrase for the key')

# open the tomb
topen('test.tomb', 'test.key', 'this is the passphrase for the key', '/tmp/tomb')

# close the tomb
tclose('test')
```

Running tests
-------------

Keep in mind that the included *test.py* file execute the
`Tomb.slam()` command which will likely close any tombs, encrypted
volumes, you may have open.


License
-------

Tomber is Copyright (c) 2014 by Federico Cardoso <reiven@gmail.com>

This package is distributed under BSD License.

See [LICENSE](https://github.com/reiven/pynientos/blob/master/LICENSE)
