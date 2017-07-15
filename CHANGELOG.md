# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Added

- System decorator
- System constructor raises TypeError if a callable is not passed
- pool property to Entity
- free() to Entity
- Check if a System is in Entity
- Private add_entity to Entity 
- Pass systems to Pool to automatically add or remove an instance to them
when you get or release an instance.
- Pool.init decorator to be used along with Pool.get
- Pool.clean decorator to be used along with Entity.free
- Entity\[type_\] for component access. Less verbose than get_component().
- Pool.free_all

### Changed

- System constructor raises a TypeError exception if a callable is not
passed.
- Pool accepts one list for variables args and another one for keywords args.
- Entity systems are stored in deque

### Deprecated

- Pool.free(). Use Entity.free() instead.
- Entity.get_component(). Use Entity\[type_\] instead.

### Removed

- Passing variable args to System constructor
- Systen.run()
- Entity get_component raises an error if belongs to a pool

### Fix

- Missing string for exception EntityBelongsToPoolError

## [2017-06-24] - 1.3.0

### Added

- System instances are now callable.
- You pass variables arguments when you call to system instances.

### Deprecated

- Assign variable arguments to System().
- System.run().

### Fixed

- Avoid possible recursion when you call a System instance.

## [2017-06-08] - 1.2.0

### Added

- args and kwargs for instancing in Pool constructor
- New tests for Pool

## [2017-06-01] - 1.1.0

### Changed
- GPL license to LGPL license.
- Pool is not an experimental feature anymore.
