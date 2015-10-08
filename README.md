# site\_scons

Platform specific configuration for cross platform builds with SCons.
The default set of configuration options that ships with SCons is very
minimal - which results in reinventing the wheel for lots of projects.

## Usage 

Add this repository as a submodule, in the same directory as your `SConstruct`

```
git submodule add git@github.com/andrewwalker/site_scons .site_scons
```

Other use-cases include adding a copy of this repository to `~/.site\_scons`

## Example

Assuming that the module is found, the following should work within scons:

```
env = CustomizedEnvironment()
env.Program('yourapp', Glob('*.cpp')
```

## Dependencies

- [SCons](www.scons.org)

## Generic Configuration

- Debug and release configurations
- Platform specific variants

  - OSX configuration

