# bbutils

Collection of code I use frequently in many of my projects. Especially the logging feature.

### Features

* Logging to console (colored) and file, in can be extended via additional writer via a plugin feature. The logging is done directly, but also can be done via a thread and a simple buffer.  

## Installation

You can install unqlite using `pip`.

    pip install bbutils

## Basic usage

Below is a sample designed to show some of the basic features and functionality of the logging library.


To begin, instantiate an ``UnQLite`` object. You can specify either the path to a database file, or use UnQLite as an in-memory database.

```pycon
>>> from unqlite import UnQLite
>>> db = UnQLite()  # Create an in-memory database.
```
