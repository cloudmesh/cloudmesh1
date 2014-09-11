from __future__ import with_statement
from fabric.api import task, local, execute, hide
import sys

__all__ = ["info", "start"]

"""usage: fab t:inventory,01 

   executes the test specified in test_inventory.py that contains 01
"""


def get_filename(name):
    '''
    greates a file name of the form test_<name>.py
    :param name: the name of the test
    '''
    return "test_{0}.py".format(name)


def find_tests(filename):
    '''
    finds all tests in a given file
    :param filename: the file to test
    '''
    filename = "tests/" + filename
    with hide('output', 'running'):
        result = local('fgrep "def" {0} | fgrep ":" | fgrep test '.format(filename),
                       capture=True).replace("def ", "").replace("(self):", "").replace(" ", "")
    return result.split("\n")


def find_classname(filename):
    '''
    finds the classname in the file
    :param filename: the filename in which to look for the class
    '''
    filename = "tests/" + filename
    with hide('output', 'running'):
        result = local('fgrep "class " {0} | fgrep ":" '.format(filename),
                       capture=True).replace("class ", "").replace(":", "").replace(" ", "")

    return result


def test(name, classname, filename):
    '''
    runs the test
    :param name: the name of the test
    :param classname: the classname of the test
    :param filename: the filename in which the nosetest is
    '''
    filename = "tests/" + filename
    print "Install package"
    with hide('output', 'running'):
        local("python setup.py install")

    local(
        "nosetests -v  --nocapture {0}:{1}.{2}".format(filename, classname, name))


@task
def start(f, name=None):
    '''
    executes a test with a given partial filename and partial name of the test
    class. the first function in the test file will be returned. for example :

    fab t:inventoy,clean 

    will look in the file test_inventory.py for the first function that has
    'clean' in its name and execute that test. The program does not support
     looking  only for @task members.


    :param f: the partial filename
    :param name: the partial name of the test task
    '''
    filename = get_filename(f)
    class_name = find_classname(filename)
    test_names = find_tests(filename)
    if name is None:
        tests = test_names
    else:
        for element in test_names:
            print element
            if name in element:
                break
        tests = [element]
    for element in tests:
        test(element, class_name, filename)


@task
def info(f=None):
    '''
    list all functions of file with the partial name f
    :param f: the name will be test_<f>.py
    '''

    if f is None:
        print "ERROR: spefifiy a test from the following list"
        with hide('output', 'running'):
            result = local(
                "ls -1 tests/test_*.py", capture=True).replace("tests/test_", "   - ").replace(".py", "")
        print "use fab test.info:<name> for more information about available tests"
        print "use fab test.start:<name>,<test> for starting a test"
        print result
        sys.exit()
    filename = get_filename(f)
    class_name = find_classname(filename)
    test_names = find_tests(filename)

    print
    print "test", class_name
    print
    print "\n".join(test_names)
