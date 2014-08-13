task
----------------------------------------------------------------------

Often you may want to execute a number of commands in parallel. This
project shows an example on how to do this easily with Celery. 

Our example creates a task that executes a shell command remotely on a
machine. However, this is just an example you can realy create other
tasks as you please.

One of the issues is how to easily stage such tasks with a number of
given parameters. To make the passing uniform, we pass all arguments
via kwargs.

In our example we simply devined a function such as::

  @app.task
  def cm_ssh(host, username, command):
      result = ssh("{0}@{1}".format(username, host), command)
      return str(result)

In our main program we can than call it with our Sequential or
parallel constructs such as 


from cloudmesh_task.parallel import Parallel, Sequential::

  hosts = ["server1.futuregrid.org",
           "server2.futuregrid.org",
           "server3.futuregrid.org",
           "server4.futuregrid.org"]

  result = Sequential(hosts, cm_ssh, 
                      username="gvonlasz", 
                      command="qstat")

  result = Parallel(hosts, cm_ssh, 
                    username="gvonlasz", 
                    command="qstat")

The first command executes the task sequentially over the array given
in the first parameter. The second one executes it in parallel


First start in one terminal the celery server::

  cm-task.py start

In a second version start the test program::

  python prg.py

