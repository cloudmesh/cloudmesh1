import fabric

@task
def on():

    debug = True
    
    fabric.state.output.debug  = debug
    fabric.state.output.running  = debug
    fabric.state.output.status  = debug
    fabric.state.output.stdout  = True
    fabric.state.output.stderr  = debug
    fabric.state.output.warnings  = debug
    fabric.state.output.aborts  = debug
    fabric.state.output.user  = debug

@task
def off():

    debug = False
    
    fabric.state.output.debug  = debug
    fabric.state.output.running  = debug
    fabric.state.output.status  = debug
    fabric.state.output.stdout  = True
    fabric.state.output.stderr  = debug
    fabric.state.output.warnings  = debug
    fabric.state.output.aborts  = debug
    fabric.state.output.user  = debug
