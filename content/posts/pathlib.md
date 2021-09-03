+++ 
draft = true
date = 2021-09-01T23:53:53-04:00
title = "The Benefits of Pathlib"
description = "Using Python's Pathlib library"
slug = ""
authors = ["Tom"]
tags = ["Python","Pathlib","os.path"]
categories = []
externalLink = ""
series = ["python"]
+++

##### Python now has a class-based way to interact with filepaths

If you have some experience using Python, you probably already know it has some good tools for ironing out the differences between Windows and Unix paths.
Provided you don't build paths like this:

{{< highlight python >}}
path = basepath + '/never' + '/do' + '/this'
{{</ highlight >}}

The tradition answer to this is to use libraries like [os](https://docs.python.org/3/library/os.html) and [os.path](https://docs.python.org/3/library/os.path.html):

{{< highlight python >}}
from os.path import join
path = join(basepath, 'a', 'better', 'path')
{{</ highlight >}}

But in terms of ease of use, these libraries are starting to show their age.
Python3 includes [pathlib](https://docs.python.org/3/library/pathlib.html), a more convinient class-based library for interacting with paths.

##### Pathlib Classes

By importing pathlib and using a Path class, we'll actually get a *concrete* class based on the underlying system.
In my case, I'm using Windows, so hopping into a Python console will return a WindowsPath.

{{< highlight python >}}
>>> from pathlib import Path
>>> pathlib_path = Path.cwd()
>>> type(pathlib_path)
<class 'pathlib.WindowsPath'>
>>> print(pathlib_path)
C:\Users\Tom\AppData\Local\Programs\Python\Python39
{{</ highlight >}}

Pathlib also has a PosixPath concrete class that you'll see used on an Ubuntu machine, for instance. 
Each concrete class is inherited from a PurePath parent class, and each PurePath class only allows path operations that don't touch the filesystem.

{{< highlight python >}}
>>> from pathlib import PurePosixPath
>>> pure_linux_path = PurePosixPath('/usr/local/bin/python3')
>>> pure_linux_path.parent
PurePosixPath('/usr/local/bin')
>>> pure_linux_path.rmdir()
Traceback (most recent call last):
File "<pyshell#63>", line 1, in <module>
pure_linux_path.rmdir()
AttributeError: 'PurePosixPath' object has no attribute 'rmdir'
{{</ highlight >}}

This can be an elegant way to do some filepath manipulation in the opposite filesystem; a necessary evil that I've sometimes run into in the CI world.

##### Console comparisons with os

One pet-peeve of mine, especially when revisiting Python after some time away, is that os.path are functions for passing in strings. 
Sometimes it is easy to forget that as my little whoops below demonstrates. 
The OOP consistency from pathlib avoids this.

{{< div/row >}}
  {{< div/column >}}
    {{< highlight python >}}
    >>> import os
    >>> path = os.getcwd()
    >>> os_path.exists()
    Traceback (most recent call last):
    File "<pyshell#11>", line 1, 
    in <module> os_path.exists()
    AttributeError: 'str' object 
    has no attribute 'exists'
    >>> os.path.exists(os_path)
    True
    {{</ highlight >}}{{</ div/column >}}
  {{< div/column >}}
    {{< highlight python >}}
    >>> from pathlib import Path
    >>> pathlib_path = Path.cwd()
    >>> pathlib_path.exists()
    True
    {{</ highlight >}}
  {{</ div/column >}}
{{</ div/row >}}

Another constant source of whoops for me is the inconsistent interface.
Directories have to do with paths so listing them must be in os.path right?


{{< div/row >}}
  {{< div/column >}}
    {{< highlight python >}}
    
    {{</ highlight >}}{{</ div/column >}}
  {{< div/column >}}
    {{< highlight python >}}
    
    {{</ highlight >}}
  {{</ div/column >}}
{{</ div/row >}}