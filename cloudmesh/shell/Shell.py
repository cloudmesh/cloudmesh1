import sh

class Shell(object):

    #    @classmethod
    #    def ls(cls, arguments=None):
    #        return cls._execute(sh.ls, arguments)
    
    
    @classmethod
    def _execute(cls, f, arguments=None):
        if arguments is None:
            return ' '.join(f().split()[-1:])
        else:
            return ' '.join(f(arguments).split()[-1:])            
                                        
    @classmethod
    def VBoxManage	(cls, arguments=None):
        return cls._execute(sh.VBoxManage, arguments)

    @classmethod
    def blockdiag	(cls, arguments=None):
        return cls._execute(sh.blockdiag	, arguments)
    
    @classmethod
    def cm(cls, arguments=None):
        return cls._execute(sh.cm, arguments)
        
    @classmethod
    def fgmetric(cls, arguments=None):
        return cls._execute(sh.fgmetric, arguments)
        
    @classmethod
    def fgrep(cls, arguments=None):
        return cls._execute(sh.fgrep, arguments)
            
    @classmethod
    def gchproject(cls, arguments=None):
        return cls._execute(sh.gchproject, arguments)
            
    @classmethod
    def gchuser(cls, arguments=None):
        return cls._execute(sh.gchuser, arguments)
                
    @classmethod
    def git(cls, arguments=None):
        return cls._execute(sh.git, arguments)
                
    @classmethod
    def glusers(cls, arguments=None):
        return cls._execute(sh.glusers, arguments)
                    
    @classmethod
    def gmkproject(cls, arguments=None):
        return cls._execute(sh.gmkproject, arguments)
                    
    @classmethod
    def grep(cls, arguments=None):
        return cls._execute(sh.grep, arguments)
                        
    @classmethod
    def gstatement(cls, arguments=None):
        return cls._execute(sh.gstatement, arguments)
                        
    @classmethod
    def head(cls, arguments=None):
        return cls._execute(sh.head, arguments)
                            
    @classmethod
    def keystone(cls, arguments=None):
        return cls._execute(sh.keystone, arguments)
                            
    @classmethod
    def kill(cls, arguments=None):
        return cls._execute(sh.kill, arguments)

    @classmethod
    def ls(cls, arguments=None):
        return cls._execute(sh.ls, arguments)
                                        
    @classmethod
    def mkdir(cls, arguments=None):
        return cls._execute(sh.mkdir, arguments)
                                    
    @classmethod
    def mongoimport(cls, arguments=None):
        return cls._execute(sh.mongoimport, arguments)
                                    
    @classmethod
    def mysql(cls, arguments=None):
        return cls._execute(sh.mysql, arguments)
                                        
    @classmethod
    def nosetests(cls, arguments=None):
        return cls._execute(sh.nosetests,pwd, arguments)
                                        
    @classmethod
    def nova(cls, arguments=None):
        return cls._execute(sh.nova, arguments)
                                            
    @classmethod
    def pwd(cls, arguments=None):
        return cls._execute(sh.pwd, arguments)
                                            
    @classmethod
    def rackdiag(cls, arguments=None):
        return cls._execute(sh.rackdiag, arguments)
                                                
    @classmethod
    def rm(cls, arguments=None):
        return cls._execute(sh.rm, arguments)
                                                
    @classmethod
    def rsync(cls, arguments=None):
        return cls._execute(sh.rsync, arguments)
                                                    
    @classmethod
    def scp(cls, arguments=None):
        return cls._execute(sh.scp, arguments)
                                                    
    @classmethod
    def sort(cls, arguments=None):
        return cls._execute(sh.sort, arguments)
                                                        
    @classmethod
    def ssh(cls, arguments=None):
        return cls._execute(sh.ssh, arguments)
                                                        
    @classmethod
    def sudo(cls, arguments=None):
        return cls._execute(sh.sudo, arguments)
                                                            
    @classmethod
    def tail(cls, arguments=None):
        return cls._execute(sh.tail, arguments)
                                                            
    @classmethod
    def vagrant(cls, arguments=None):
        return cls._execute(sh.vagrant, arguments)
                                                                
if __name__ == "__main__":
    print Shell.ls("-1")
    print Shell.ls()
    print Shell.ls(["-A", "-G"])    

    print Shell.pwd()

