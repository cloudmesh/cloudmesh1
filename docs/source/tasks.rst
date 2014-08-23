.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 5

..

Issue Management
======================================================================

We will be using git issue task list to manage assignments to
projects.  Previously we have used jira for this, but it is just
easier to use the build in issue management system. Unfortunately, the
issue management system has a couple of limitations that we try to
overcome by introducing additional labels.

Labels
----------------------------------------------------------------------

:z-user: 
    although github has assignees, its not easily possible to see to
    whom the issue is assigned as we could not figure out how to use
    usernames instead of the gravatar image. Additionally, sometimes
    an issue requires that two people work on it and with name labels
    we can do so.

:active: 
    the active label is to be set when we work on an issue

:help: 
    sometimes you may need help on an issue, if you do, you can use
    his label and put in the comment what you need help with. This is
    useful in case we are not all in the same building and need to
    move forward quickly

:bug: 
    a simple bug that we know is wrong and needs fixing

:review: 
    sometimes a task needs a review before it is completed. This label
    will notify Gregor to conduct a review. It is less urgent than the
    **help** label.

Priority
----------------------------------------------------------------------

So fare priorities are managed by milestone, but in future we may
introduce priority categories form 1-5 which are just numbers. THis
way we can see on what we should spend our time.

Inactivity
----------------------------------------------------------------------

It is important that everyone engages in taking tasks and solving them
and if we get stuck get other involved. It is not helpful if you were
to just passively wait for tasks. when you are done come and pick up
the next task.

Shortcuts
----------------------------------------------------------------------

* `List of open issues <https://github.com/cloudmesh/cloudmesh/issues?direction=desc&sort=updated&state=open>`_
* `Milestones <https://github.com/cloudmesh/cloudmesh/issues/milestones>`_
* `Oholo <https://www.ohloh.net/p/cloudmesh-rain>`_

Examples of user specific shortcuts

* `List all open tasks assigned to Gregor <https://github.com/cloudmesh/cloudmesh/issues/assigned/laszewsk?direction=desc&sort=updated&state=open>`_
* `List all open tasks with the label Gregor <https://github.com/cloudmesh/cloudmesh/issues/assigned/laszewsk?direction=desc&labels=z-gregor&page=1&sort=updated&state=open>`_

* `List all currently active tasks <https://github.com/cloudmesh/cloudmesh/issues/assigned/laszewsk?direction=desc&labels=active&page=1&sort=updated&state=open>`_

* `List tasks that need help <https://github.com/cloudmesh/cloudmesh/issues/assigned/laszewsk?direction=desc&labels=help&page=1&sort=updated&state=open>`_

* `List tasks that need review  <https://github.com/cloudmesh/cloudmesh/issues/assigned/laszewsk?direction=desc&labels=review&milestone=&page=1&sort=updated&state=open>`_

