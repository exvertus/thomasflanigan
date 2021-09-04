+++ 
draft = false
date = 2021-09-01T23:53:53-04:00
title = "The Advantages of Pathlib"
description = "Using Python's Pathlib library"
slug = ""
authors = ["Tom"]
tags = ["Python","Pathlib","os.path"]
categories = []
externalLink = ""
series = ["python"]
+++

#### Python3 has a standard library with classes for filepaths. Are you using it yet?

If you have some experience using Python, you probably already know it has some good tools for ironing out differences between Windows and Unix paths, provided you don't build paths like this:

{{< highlight python >}}
path = basepath + '/never' + '/do' + '/this'
{{</ highlight >}}

The traditional answer has been to use libraries like [os](https://docs.python.org/3/library/os.html) and [os.path](https://docs.python.org/3/library/os.path.html):

{{< highlight python >}}
from os.path import join
path = join(basepath, 'a', 'better', 'path')
{{</ highlight >}}

But in terms of ease of use, these libraries are starting to show their age.
Python3 includes [pathlib](https://docs.python.org/3/library/pathlib.html), a more convenient class-based library for interacting with paths.

##### Pathlib Classes

By importing ```pathlib``` and using a Path class, we'll get a *concrete* class based on the underlying filesystem.
In my case, I'm using Windows. Testing in a Python console will return a WindowsPath.

{{< highlight python >}}
>>> from pathlib import Path
>>> pathlib_path = Path.cwd()
>>> type(pathlib_path)
<class 'pathlib.WindowsPath'>
>>> print(pathlib_path)
C:\Users\Tom\AppData\Local\Programs\Python\Python39
{{</ highlight >}}

```pathlib``` also has a ```PosixPath``` concrete class that you'll get from calling ```Path()``` on an Ubuntu machine, for instance. 
Each concrete class is inherited from a ```PurePath``` parent, and each ```PurePath``` class allows path operations, provided they don't touch the filesystem, which will error.

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

This can be an elegant way to do some filepath manipulation in the opposite platform; a necessary evil that I've sometimes run into for cross-platform CI projects.

##### Console comparisons with os

One pet-peeve of mine, especially when revisiting Python after some time away, is that ```os.path``` contains functions instead of methods. 
It is easy to forget that as my little whoops below demonstrates. 
The OOP consistency from ```pathlib``` avoids this.

{{< div/row >}}
{{< div/column >}}
{{< highlight python >}}
>>> import os
>>> os_path = os.getcwd()
>>> os_path.exists()
Traceback (most recent call last):
File "<pyshell#11>", line 1, 
in <module> os_path.exists()
AttributeError: 'str' object has no attribute 'exists'
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

Another source of errors is the inconsistent interface.
Directories have to do with paths, so the function for listing them must be in ```os.path```, right?

{{< div/row >}}
{{< div/column >}}
{{< highlight python >}}
>>> os.path.listdir(os_path)
Traceback (most recent call last):
File "<pyshell#19>", line 1, in <module>
os.path.listdir(os_path)
AttributeError: module 'ntpath' has no attribute 'listdir'
>>> os.listdir(os_path)
['DLLs', 'Doc', ...]
{{</ highlight >}}{{</ div/column >}}
{{< div/column >}}
{{< highlight python >}}
>>> list(pathlib_path.iterdir())
[WindowsPath('C:/Users/Tom/AppData/Local/Programs/Python/Python39/DLLs'), 
 WindowsPath('C:/Users/Tom/AppData/Local/Programs/Python/Python39/Doc'),
 ...]
{{</ highlight >}}
{{</ div/column >}}
{{</ div/row >}}

```pathlib``` also provides some convenient attributes, retrieving values related to the path is as simple as it should be.
Some of the terminology ```pathlib``` uses for paths can be quickly understood by looking at the [pathlib cheatsheet](https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf).

{{< div/row >}}
{{< div/column >}}
{{< highlight python >}}
>>> os_home = os.path.expanduser('~Tom')
>>> os.path.basename(os_home)
'Tom'
>>> os.path.dirname(os_home)
'C:\\Users'
>>> os.path.splitext(os.path.join(os_home, 'test.txt'))[1]
'.txt'
{{</ highlight >}}{{</ div/column >}}
{{< div/column >}}
{{< highlight python >}}
>>> pathlib_home = Path('~Tom').expanduser()
>>> pathlib_home.name
'Tom'
>>> pathlib_home.parent
WindowsPath('C:/Users')
>>> Path(pathlib_home, 'test.txt').suffix
'.txt'
{{</ highlight >}}
{{</ div/column >}}
{{</ div/row >}}

##### Final examples

So while it is still important to avoid code like this:

{{< highlight python >}}
path = basepath + '/never' + '/do' + '/this'
{{</ highlight >}}

It is easy to understand the temptation, which brings me to my conclusion:
```pathlib``` enables me to think about paths the way I already do, *without* the hurdles of a dispersed interface.
Below I've simplified a scenario I've encountered working on a CI project, again comparing ```os``` with the same logic refactored for ```pathlib```.

{{< highlight python >}}
import os
info_folder = os.path.join(os.environ.get('WORKSPACE', '.'), 'build', 'info')
os.makedirs(info_folder, exist_ok=True)
project.build()
with open(os.path.join(info_folder, 'results.xml')) as f:
    xml_results = f.read()
with open(os.path.join(info_folder, 'build_log.txt')) as f:
    build_log = f.read()
{{</ highlight >}}

{{< highlight python >}}
from pathlib import Path
workspace = Path(os.environ.get('WORKSPACE', '.'))
(workspace/'build'/'info').mkdir(parents=True, exist_ok=True)
project.build()
xml_results = (workspace/'build'/'info'/'results.xml').read_text()
build_log = (workspace/'build'/'info'/'build_log.txt').read_text()
{{</ highlight >}}

With ```os```, I'm almost forced to over-name things to keep the verbosity down, hence the 'info_folder' variable.
There really isn't a need for such a variable when using ```pathlib```.
I can use forward slashes on either platform and ```pathlib``` will manage the differences behind the scenes.
This matches Java/Groovy behavior I've used in [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/) before too, so switching languages feels smoother.
I can get back to how I actually think about the path and see the portion I care about, under one library of consistently named methods.
Which of the above would you rather read?

If that isn't enough to convince you to change your code to ```pathlib```, there is also the flexibility of partially swapping out ```pathlib``` without having to adjust for each new ```pathlib``` method.
Thanks to [PEP 519](https://www.python.org/dev/peps/pep-0519/) and the [PathLike](https://docs.python.org/3/library/os.html#os.PathLike) base class, ```pathlib``` paths resolve to strings and can be used as arguments to built-in functions as if they were the path strings from ```os``` functions.

{{< highlight python >}}
>>> with open(os.path.join(os.path.expanduser('~Tom'), 'test.txt')) as f:
...     x = f.read()
...
>>> with open(Path.home()/'test.txt') as f:
...     y = f.read()
...
>>> with (Path.home()/'test.txt').open() as f:
...     z = f.read()
...
>>> min(x == y, y == z)
True
{{</ highlight >}}

So while using classes instead strings comes with a bit more resource overhead, the reduction in errors and readability you get from ```pathlib``` is usually well worth it.
I would love to see more code use ```pathlib```, so if you aren't already using it, I hope this post has swayed you.

