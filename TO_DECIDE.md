
# TO DECIDE

This file is a record of some items that require decisionmaking on the part of the project.

These will be noted here while the project is in the prototyping phase, so that they can be returned to as necessary, or, when the project is more mature.

Ideally, the result of these decisions would be encoded as Architecture Decision Records in ./docs/architecture as currently proposed there.

## OS-support

Currently, this project is has been seeded in a way that would require symlinks to work properly, as a way of centralizing package-definitions to the point that a single package-def and build script can be used to build all versions in the platform as much as possible. However, Windows support for symlinks is lacking, and we will need to make accommodations, so when we get to the point of supporting Windows, how ought we handle symlinks will need to be decided upon?

## Offline Downloads

Should this project should support offline-source-retrieval for the benefit of those who are located on the harsh end of a firewall?

## Purpose

Is this project primarily designed to act as a minimal reference, useful for small studios just starting, act as a medium reference, for larger groups looking to adopt the full power of rez, or act as a mega reference, interoperable with large studios that know what they are doing, but want to adopt best-practices as outlined in this reference project?


