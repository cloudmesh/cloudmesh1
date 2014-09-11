import fabric
from fabric.api import task


@task
def on():

    _debug = False

    fabric.state.output._debug = _debug
    fabric.state.output.running = _debug
    fabric.state.output.status = _debug
    fabric.state.output.stdout = _debug
    fabric.state.output.stderr = _debug
    fabric.state.output.warnings = _debug
    fabric.state.output.aborts = _debug
    fabric.state.output.user = _debug


@task
def off():

    _debug = True

    fabric.state.output._debug = _debug
    fabric.state.output.running = _debug
    fabric.state.output.status = _debug
    fabric.state.output.stdout = _debug
    fabric.state.output.stderr = _debug
    fabric.state.output.warnings = _debug
    fabric.state.output.aborts = _debug
    fabric.state.output.user = _debug
