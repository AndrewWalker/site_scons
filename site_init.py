""" SCons basic build flags for cross platform compilations


"""
import os
import sys

def configure_darwin(env):
    """ Configure for recent (Yosemite or better) versions of OSX
    """

    warnings = ''
    warnings += '-Wall -Wextra -Wpedantic -Wwrite-strings '
    warnings += '-Wcast-qual -Wconversion -Werror=return-type'
    warnings = warnings.split()
    env['WARNINGFLAGS'] = warnings
    env.Append(CCFLAGS = '$WARNINGFLAGS')

    # if scons is being run as a tool (say from inside vim)
    # don't worry about coloring the output
    if sys.stdout.isatty():
        env.Append(CCFLAGS = ['-fcolor-diagnostics'])

    env.Append(CXXFLAGS = '-std=c++1y -stdlib=libc++'.split())

    opt_flags = dict(
        debug   = '-g -O0'.split(),
        release = ['-03']
    )

    configuration = env.subst('$configuration').lower()
    env.Append(CCFLAGS = opt_flags[configuration])
    return env


def configure_windows(env):
    """ Configure windows / visual studio
    """
    env.Append(CPPDEFINES = ['WIN32'])
    env.Append(CCFLAGS = '/W3 /Gd /nologo /RTC1 /sdl /EHsc /GS /fp:precise'.split())
    env.Append(LINKFLAGS = '/nologo')
    if 'debug' == env.subst('$configuration').lower():
        env.Append(CPPDEFINES = ['_DEBUG'])
        env.Append(CCFLAGS = '/Od'.split())
        if 'static' == env.subst('$msvc_crt'):
            env.Append(CCFLAGS = '/MTd')
        else:
            env.Append(CCFLAGS = '/MDd')
    if 'release' == env.subst('$configuration').lower():
        env.Append(CPPDEFINES = ['NDEBUG'])
        env.Append(CCFLAGS = '/O2'.split())
        if 'static' == env.subst('$msvc_crt'):
            env.Append(CCFLAGS = '/MT')
        else:
            env.Append(CCFLAGS = '/MD')


def configure_platform(env):
    platforms = {
        'darwin' : configure_darwin,
        'win32'  : configure_windows
    }
    platforms[sys.platform](env)


def CustomizedEnvironment(env = None, **kwargs):
    """Customized environment configuration
    """

    vars = kwargs.get('variables', Variables(None, ARGUMENTS))
    vars.Add('configuration', 'select debug or release', 'debug')
    vars.Add('platform', 'host platform to use', sys.platform)
    kwargs['variables'] = vars

    if env is None:
        env = SCons.Script.Environment(**kwargs)

    configure_platform(env)

    # Add an output location for VariantDir
    env['BUILDDIR'] = '#build/$platform/$configuration'
    env['BINDIR'] = '#bin'

    Help(vars.GenerateHelpText(env))
    return env


