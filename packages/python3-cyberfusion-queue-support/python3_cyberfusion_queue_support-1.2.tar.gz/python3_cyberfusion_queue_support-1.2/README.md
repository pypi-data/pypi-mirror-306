# python3-cyberfusion-queue-support

Library to queue actions.

# Concepts

All project-specific terms are in _italic_.

After creating a _queue_, _items_ can be added to it.

```python
queue = Queue()

queue.add(item)
```

These _items_ can be of multiple types such as `ChmodItem` or `SystemdUnitRestartItem`, and they can have attributes such as a path for an `MkdirItem` or a unit name for a `SystemdUnitEnableItem`.

```python
item1 = ChmodItem(path="/tmp/example.txt", mode=0o600)
item2 = SystemdUnitEnableItem(name="httpd.service")
```

Each _item_ type has one or multiple _outcomes_ that should come true for an _item_ of that type to be completed. For example: for an _item_ of type `UnlinkItem`, the _outcome_ is that the file at the path given with the _item_ is unlinked.

When a _queue_ is _processed_, all the _items_ added to it are _fulfilled_, meaning all the _items'_ _outcomes_ are completed.

```python
item = RmTreeItem(path="/tmp/dir")

queue = Queue()

queue.add(item)

# for each item added to the queue, its fulfill() function is run
queue.process()

# this would do the same
item.fulfill()
```

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-queue-support

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Example

```python
from cyberfusion.QueueSupport import Queue
from cyberfusion.QueueSupport.items.chmod import ChmodItem

queue = Queue()

item = ChmodItem(path="/tmp/example.txt", mode=0o600)
print(item.outcomes)

queue.add(item)

preview = True or False

outcomes = queue.process(preview=preview)

for outcome in outcomes:
    print(str(outcome))
```
