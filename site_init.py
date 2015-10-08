""" SCons basic build flags for cross platform compilations


"""
import os


def configure_darwin(env):
    """ Configure for recent (Yosemite or better) versions of OSX
    """

    warnings = ''
    warnings += '-Wall -Wextra -Wpedantic -Wwrite-strings '
    warnings += '-Wcast-qual -Wconversion -Werror=return-type'
    warnings = warnings.split()

    env['WARNINGFLAGS'] = warnings
    env.Append(CCFLAGS = ['-fcolor-diagnostics $WARNINGFLAGS'])
    env.Append(CXXFLAGS = '-std=c++1y -stdlib=libc++'.split())

    opt_flags = dict(
        debug   = '-g -O0'.split(),
        release = ['-03']
    )

    configuration = env.subst('$configuration').lower()
    env.Append(CCFLAGS = opt_flags[configuration])
    return env


def configure_platform(env):
    platforms = {
        'darwin' : configure_darwin
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


