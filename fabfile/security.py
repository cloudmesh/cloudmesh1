from fabric.api import task, local
from build import cursor_on


@task
def check(search=""):
    check_list = [("openstack", "'OS_PASSWORD': '[a-zA-Z0-9]+'"),
                  ("aws", "'EC2_SECRET_KEY': '[a-zA-Z0-9]+'")]
    for pair in check_list:
        platform = pair[0]
        _search = pair[1]
        _grep(_search, platform)
    if search:
        _grep(search, 'CUSTOMIZED_SEARCH')
    cursor_on()


def _grep(search, platform):
    if not search:
        search = "'OS_PASSWORD': '[a-zA-Z0-9]+'"
    cmd = "egrep -ri \"{0}\" * | cut -d\":\" -f1".format(search)
    print("[{0}]:{1}".format(platform, cmd))
    res = local(cmd, capture=True)
    if res:
        print ('[{0}]: [ERROR] PASSWORD(OR SECRET KEY) DETECTED, SEE FILES '
               'BELOW'.format(platform))
        print ("")
        print (res)
    else:
        print ("[{0}]: NO PASSWORD DETECTED".format(platform))

    print ("")
