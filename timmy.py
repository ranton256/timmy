import os
import pygame
import sys
from types import ModuleType

from pgzero.runner import prepare_mod, run_mod

# TODO: this works except for drawing text, don't think it can find the fonts
def main(path, repl=False):
    """Run a PygameZero module, with the path specified by the program.
    (Other than that, this is identical to the regular main() from runner.py)
    """
    with open(path) as f:
        src = f.read()

    print(os.path.basename(path))
    code = compile(src, os.path.basename(path), 'exec', dont_inherit=True)
    
    name, _ = os.path.splitext(os.path.basename(path))
    mod = ModuleType(name)
    mod.__file__ = path
    mod.__name__ = name
    sys.modules[name] = mod

    # tell main code not to do pgzrun
    os.environ['pyi'] = 'pyi'

    # Indicate that we're running with the pgzrun runner
    # This disables the 'import pgzrun' module
    sys._pgzrun = True

    prepare_mod(mod)
    exec(code, mod.__dict__)
    #run_mod(mod, repl=repl)
    run_mod(mod)

# Need the full path if we're loading a file and compiling it
main( os.path.join(sys._MEIPASS, "timmy1.py") )
