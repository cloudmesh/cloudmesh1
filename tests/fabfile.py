from fabric.api import task, local, execute

"""usage: fab t:inventory,01 

   executes the test specified in test_inventory.py that contains 01
"""


def find_filename(name):
    return "test_{0}.py".format(name)
    
def find_tests(filename):
    result = local('fgrep "def" {0} | fgrep ":" | fgrep test '.format(filename),
                   capture = True).replace("def ", "").replace("(self):", "").replace(" ", "")
    return result.split("\n") 
    
def find_classname(filename):
    result = local('fgrep "class " {0} | fgrep ":" '.format(filename),
                   capture = True).replace("class ", "").replace(":", "").replace(" ", "")

    return result
    
def test(name,classname,filename):
    local("cd ..; python setup.py install")
    local("nosetests -v  --nocapture {0}:{1}.{2}".format(filename, classname, name))

@task
def t(f,name):
    filename = find_filename(f)
    class_name = find_classname(filename)
    test_names  = find_tests(filename) 
    for element in test_names:
        print element
        if name in element:
            break
    print element
    print filename
    print class_name
    test (element, class_name,filename)

@task
def i(f):
    filename = find_filename(f)
    class_name = find_classname(filename)
    test_names  = find_tests(filename) 

    print
    print "test", class_name
    print
    print "\n".join(test_names)
    

    

   
