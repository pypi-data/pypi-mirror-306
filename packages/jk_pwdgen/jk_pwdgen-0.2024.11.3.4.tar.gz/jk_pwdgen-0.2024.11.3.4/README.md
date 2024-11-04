jk_pwdgen
==========

Introduction
------------

This python module provides support for password generation.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-pwdgen)
* [pypi.python.org](https://pypi.python.org/pypi/jk_pwdgen)

Why this module?
----------------

Every user needs strong passwords for various services used. Especially system administrators need passwords of good quality. This python module provides ways to easily generate strong passwords locally.

Limitations of this module
--------------------------

The implementations provided here makes use of default implementations of random number generators in Python. This is a Mersenne Twister and uses `/dev/urandom`. The quality of randomness is limited to the quality of the underlying implementation in Python. We should assume that the underlying implementation in Python is sufficiently tested and does not contain severe bugs. However it is important to realize that the quality of this underlying implementation is a limiting factor.

What is a (sufficiently) good password
----------------------

Good passwords ...:

- **should be random**. The more random the better. Passwords that contain words which can be found in a human readable dictionary aren't very good.
- **should contain numbers**. This increases the complexity.
- **should contain special characters**. This increases the complexity as well.
- **should not contain a high variety of characters**. This as well increases the complexity.

The password generator provided here aims to meet these criteria.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_pwdgen
```

### Instantiate a password generator

Now you can instantiate a password generator (and configure it as desired):

```python
pwdGen = jk_pwdgen.PasswordGenerator()
pwdGen.setLength(24)
```

### Generate a password

A password can then be generated like this:

```python
print(pwdGen.generate())
```

How to use the standalone tool
----------------------

### Run the password generator

This module comes with a standalone program named `pwdgen.py`. After installing this module you should be able to invoke it via command line. It basically performs exactly those steps described above in order to generate a password. Just execute `pwdgen.py` such as this:

```
$ pwdgen.py
mS-UMb5JGSd.LVwszF54Hw~v
$ _
```

### Help text

For more details run `pwdgen.py -h` to display this help text:

```
pwdgen [options] - Generate strong passwords.

  Description:

    This tool assists in the generation of strong passwords. Generation is based on the Python
    random number generator random.Random. According to the Python documentation this RNG is
    based on Mersenne Twister and os.urandom(), so it should provide sufficient randomness for
    password generation.

    This tool will verify that passwords generated are of sufficient by verifying that the
    correct number of special characters as well as enough numeric characters are present in
    the password generated.

    In order to use this password generation tool just run it. On each run it will generate
    one or more passwords (depending on arguments specified). All passwords are printed to
    STDOUT line by line.

  Options:

    -h    --help                       Display this help text.
    -n n                               Number of passwords to generate. (Default: 1)
    -l n  --length n                   Length of password to generate. (Default: 24)
          --minNumberOfNumericChars n  Minimum number of numeric characters. (Default: 2)
          --numberOfSpecialChars n     Minimum number of special characters. (Default: 3)
          --prohibitedChars s          Prohibites characters. (Default: "0l")

  Author:

    Jürgen Knauth <jk@binary-overflow.de>

  Return codes:

    0  Everything is okay.
    1  An error occurred.

  License:

    This program is free software: you can redistribute it and/or modify it under the terms of
    the Apache Software License as published by Apache Software Foundation in version 2. For
    more details see the Apache Software License, which should be vailable at:
    https://www.apache.org/licenses/LICENSE-2.0
```

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



