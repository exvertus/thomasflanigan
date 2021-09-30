+++ 
draft = true
date = 2021-09-14T13:24:07-04:00
title = "Unittests and the Filesystem"
description = "Using pytest and pyfakefs for unit tests"
slug = ""
authors = ["Tom"]
tags = ["Python","pytest","pyfakefs"]
categories = []
externalLink = ""
series = ["python"]
+++

##### Is faking the filesystem _really_ worth it?

I haven't found much consensus around this topic.

Some might claim (_emphasis_ mine):

{{< url-quotation source="Michael Feathers" url="https://www.artima.com/weblogs/viewpost.jsp?thread=126923">}}
A test is not a unit test if:

* It talks to the database
* It communicates across the network
* _It touches the file system_
* It can't run at the same time as any of your other unit tests
* You have to do special things to your environment (such as editing config files) to run it
{{< /url-quotation >}}

There are a couple of reasons for only incorporating these at the integration and end-to-end test stage.

The first is speed.
A slow test is one that is rarely run, and in many cases would not have much value for local development, or even continuous integration branch builds.
Having a suite of tests that can provide near-instant feedback is important for maintaining good developer flow.

I other reason is isolation.

Incorporating more than the code under test in my unit tests means I can't be sure my code vs something else broke when tests fail.

While things like a networked database might require test doubles for speed, how much does it really matter about the filesystem?
It may be annoying for a developer to run a local database, but what development environment isn't going be able to read, write, and create files and directories?

Well it is not necessarily a bad practice to take a more pragmatic approach, as [martinfowler.com](https://martinfowler.com/) notes (again _emphasis_ mine)...

{{< url-quotation source="Ham Vocke, _The Practical Test Pyramid_" url="https://martinfowler.com/articles/practical-test-pyramid.html#SociableAndSolitary">}}
Some argue that all collaborators (e.g. other classes that are called by your class under test) of your subject under test should be substituted with mocks or stubs to come up with perfect isolation and to avoid side-effects and a complicated test setup. Others argue that _only collaborators that are slow or have bigger side effects_ (e.g. classes that access databases or make network calls) should be stubbed or mocked.
{{< /url-quotation >}}

So in many cases, the filesystem is the least of our concerns.
But so far I've haven't addressed a key variable out of the cost side.

##### How difficult is it to mock the filesystem?

So in order to know whether mocking the filesystem is really worth it, we first need to know how difficult it is.
That of course is going to depend on the language we're using and tools available. 
I don't have time to do an exhaustive comparison here, so I'll pick python and pytest and explore a couple options.

I'll use a trivial example to test against:

{{< highlight python >}}
# touch.py
import pathlib

def touch(target_path):
    path = pathlib.Path(target_path)
    print(f"creating {path}")
    path.touch()

{{</ highlight >}}

There isn't really any code under test to speak of here, but since I'm just testing out options at this point, I'll keep things as simple as possible.
All this function does really is use `pathlib` (see [my last post](/posts/pathlib/) for more) to create a single file.

###### Mocking pathlib

I could mock `pathlib.Path` itself to avoid using the filesystem.

{{< highlight python >}}
import os
import pytest
from unittest.mock import patch, Mock

import touch

@patch('pathlib.Path')
def test_mocked_touch(mock_path):
    touch.touch('./mocked-touch.test')
    assert mock_path.called_with('./mocked-touch.test')
    # Make sure it didn't use the filesystem
    assert not os.path.exists('./mocked-touch.test')

{{</ highlight >}}

This should work well enough and is easy to implement.
But there is one small thing I don't like about it.

This patch and `mock_path.called_with` assertion assumes I am using pathlib.
If I swap out how I am creating the file (for example calling something that using `os` instead of `pathlib`) I will have to update my test as well.

It would be nice if my test were a little more black-boxy and for this I would need something more like a fake than a mock.

###### Pyfakefs

Googling for a solution quickly turned up [pyfakefs](https://github.com/jmcgeheeiv/pyfakefs).
It provides a full filesystem implementation, but running in memory.

It allows me to pass an fs object modeling a real filesystem, with supporting methods to interact with the fake filesystem.
It will also swap things like pathlib, os, and most other things that don't use C libraries to talk to the filesystem.

{{< highlight python >}}
import pytest
import pyfakefs

import touch

def test_touch(fs):
    touch.touch('./pyfakefs.txt')
    assert fs.exists('./pyfakefs.txt')

{{</ highlight >}}

This greatly simplifies my code and I'm not using spy methods like `called_with` that couple my test code to what library I use internally.

##### Basically free is worth it

So I think as far as python goes I'm in the Michael Feathers camp on this one.
Pyfakefs (available on [PyPi](https://pypi.org/project/pyfakefs/)) makes this so pain-free that I don't see a reason to cheat on the filesystem for unittests.
