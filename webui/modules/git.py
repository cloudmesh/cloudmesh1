import envoy
from flask import Blueprint
from flask import render_template
from sh import git

git_module = Blueprint('git_module', __name__)


@git_module.route('/git/')
def display_git_authors():
    result = git("shortlog", "-s", "-n",
                 _tty_in=True, _tty_out=False).split("\n")
    authors = {}
    for line in result:
        print line
        try:
            (commits, name) = line.split("\t")
            authors[name] = {"name": name, "commits": commits}
        except:
            print "error:", line

    result = envoy.run('git log --all --format=\"%aN <%cE>\" | sort -u')
    print result.std_out
    print "abc", result.__dict__
    """
    for line in result:
        print line
        try:
            (name, email) = line.split("\t")
            authors[name]["email"] = email
        except:
            print "error:", line

    print authors
    """
    return render_template('git.html', authors=authors)
