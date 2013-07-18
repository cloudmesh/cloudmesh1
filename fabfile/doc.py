from fabric.api import task, local

@task
def build():
	local("cd doc; make html")
	local("open doc/build/html/index.html")

@task
def gh():
	local("git checkout gh-pages")
	local("make pages")
