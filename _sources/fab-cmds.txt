fabric commands
===============



===================== ======================================================================================== =====================================
available commands         description                                                                          result
--------------------- ---------------------------------------------------------------------------------------- -------------------------------------
build.fast            install cloudmesh                       
build.install         install cloudmesh
build.sdist           create the sdist
build.sphinx
clean.all             clean the dis and uninstall cloudmesh
clean.dir             clean the dirs
doc.gh                deploy the documentation on gh-pages
doc.html
doc.man               deploy the documentation on gh-pages
doc.view              view the documentation in a browser
git.gregor            git config of name and email for gregor
git.pull              git pull
git.push              git push
hpc.all               clean the dis and uninstall cloudmesh
hpc.touch             clean the dirs
iptable.info
iptable.port
iptable.production
mongo.admin           creates a password protected user for mongo
mongo.boot
mongo.clean
mongo.cloud           puts a snapshot of users, servers, images, and flavors into mongo
mongo.errormetric     puts an example of a log file into the mongodb logfile
mongo.info
mongo.install         installs mongo in ~/ENV/bin. Make sure your path is set correctly
mongo.inventory
ongo.kill
mongo.ldap            fetches a user list from ldap and displays it
mongo.metric          puts an example of a log file into the mongodb logfile
mongo.pbs
mongo.projects
mongo.simple          puts a snapshot of servers, images, and flavors into mongo (no users)
mongo.start           start the mongod service in the location as specified in
mongo.stop            stops the currently running mongod
mongo.users           puts a snapshot of the users into mongo
mongo.vms_find
mongo.wipe            wipes out all traces from mongo
mooc.start
mq.allow              allow a user to access the host in rabitmq
mq.check              check if the /etc/hosts file is properly configures
mq.dns                restart the dns server
mq.host               adding a host to rabitmq
mq.info               print some essential information about the messaging system
mq.install
mq.menu               open a menu to start some commands with an ascii menu
mq.start              start the rabit mq server
mq.status             print the status of rabbitmq
mq.stop               stop the rabit mq server
mq.user               create a user in rabit mq
nose.install          install nose-json
nose.run              run the nosetests
nose.view
pep8.auto             run autopep8 on all python files
pep8.install          install pep8, autopep8, pylint
pep8.stat             create statistics for pep8
pypi.register         register with pypi. Needs only to be done once.
pypi.upload           upload the dist to pypi
queue.clean           stop celery and clean up
queue.gui             start the flower celery gui
queue.kill
queue.list            list the workers
queue.ls
queue.lspbs
queue.monitor         provide some information about celery
queue.start           start the celery server
queue.stop            stop the workers
rcfile.download
server.agent
server.clean          clean the directory
server.kill           kills all server processes
server.quick          starts in dir webgui the program server.py and displays a browser on the given port and link
server.start          starts in dir webgui the program server.py and displays a browser on the given port and link
server.stop           sma e as the kill command
server.view           run the browser
server.wsgi
test.info             list all functions of file with the partial name f
test.start            executes a test with a given partial filename and partial name of the test
tunnel.flask
tunnel.kill
tunnel.ldap
tunnel.open           clean the dirs
user.delete_defaults
user.mongo
user.password
user.register
========================= ====================================================================================================================================================== ================
