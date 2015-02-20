import sh

class Shell(object):

    #    @classmethod
    #    def ls(cls, arguments=None):
    #        return cls._execute(sh.ls, arguments)
    
    
    @classmethod
    def _execute(cls, f, *arguments):
        args = list(*arguments)
        if len(args) == 0:
            return f().rstrip('\n')
        else:
            return f(args).rstrip('\n')
                                        
    @classmethod
    def VBoxManage	(cls, *arguments):
        return cls._execute(sh.VBoxManage, arguments)

    @classmethod
    def blockdiag	(cls, *arguments):
        return cls._execute(sh.blockdiag	, arguments)
    
    @classmethod
    def cm(cls, *arguments):
        return cls._execute(sh.cm, arguments)
        
    @classmethod
    def fgmetric(cls, *arguments):
        return cls._execute(sh.fgmetric, arguments)
        
    @classmethod
    def fgrep(cls, *arguments):
        return cls._execute(sh.fgrep, arguments)
            
    @classmethod
    def gchproject(cls, *arguments):
        return cls._execute(sh.gchproject, arguments)
            
    @classmethod
    def gchuser(cls, *arguments):
        return cls._execute(sh.gchuser, arguments)
                
    @classmethod
    def git(cls, *arguments):
        return cls._execute(sh.git, arguments)
                
    @classmethod
    def glusers(cls, *arguments):
        return cls._execute(sh.glusers, arguments)
                    
    @classmethod
    def gmkproject(cls, *arguments):
        return cls._execute(sh.gmkproject, arguments)
                    
    @classmethod
    def grep(cls, *arguments):
        return cls._execute(sh.grep, arguments)
                        
    @classmethod
    def gstatement(cls, *arguments):
        return cls._execute(sh.gstatement, arguments)
                        
    @classmethod
    def head(cls, *arguments):
        return cls._execute(sh.head, arguments)
                            
    @classmethod
    def keystone(cls, *arguments):
        return cls._execute(sh.keystone, arguments)
                            
    @classmethod
    def kill(cls, *arguments):
        return cls._execute(sh.kill, arguments)

    @classmethod
    def ls(cls, *arguments):
        return cls._execute(sh.ls, arguments)
                                        
    @classmethod
    def mkdir(cls, *arguments):
        return cls._execute(sh.mkdir, arguments)
                                    
    @classmethod
    def mongoimport(cls, *arguments):
        return cls._execute(sh.mongoimport, arguments)
                                    
    @classmethod
    def mysql(cls, *arguments):
        return cls._execute(sh.mysql, arguments)
                                        
    @classmethod
    def nosetests(cls, *arguments):
        return cls._execute(sh.nosetests,pwd, arguments)
                                        
    @classmethod
    def nova(cls, *arguments):
        return cls._execute(sh.nova, arguments)
                                            
    @classmethod
    def pwd(cls, *arguments):
        return cls._execute(sh.pwd, arguments)
                                            
    @classmethod
    def rackdiag(cls, *arguments):
        return cls._execute(sh.rackdiag, arguments)
                                                
    @classmethod
    def rm(cls, *arguments):
        return cls._execute(sh.rm, arguments)
                                                
    @classmethod
    def rsync(cls, *arguments):
        return cls._execute(sh.rsync, arguments)
                                                    
    @classmethod
    def scp(cls, *arguments):
        return cls._execute(sh.scp, arguments)
                                                    
    @classmethod
    def sort(cls, *arguments):
        return cls._execute(sh.sort, arguments)
                                                        
    @classmethod
    def ssh(cls, *arguments):
        return cls._execute(sh.ssh, arguments)
                                                        
    @classmethod
    def sudo(cls, *arguments):
        return cls._execute(sh.sudo, arguments)
                                                            
    @classmethod
    def tail(cls, *arguments):
        return cls._execute(sh.tail, arguments)
                                                            
    @classmethod
    def vagrant(cls, *arguments):
        return cls._execute(sh.vagrant, arguments)
                                                                
if __name__ == "__main__":
    print Shell.ls("-1")
    print Shell.ls()
    print Shell.ls("-A", "-G")    

    print Shell.pwd()

