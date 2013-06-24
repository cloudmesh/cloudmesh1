from pprint import pprint
from sh import git
from sh import sort
from sh import grep

class GitInfo:

    def version(self):
        return str(git.describe("--tags"))[:-1]

    def emails(self,format=None):
        if format==None:
            format_string = "'%aN' <%cE>"
        elif format == 'dict':
            format_string = "%aN\t%cE"
        result = sort (git.log("--all", "--format=" + format_string, _tty_in=True, _tty_out=False, _piped=True), "-u")

        if format == None:
            return result
        elif format == "dict":
            list = result.replace("\n", "\t").split("\t")[:-1]
            it = iter(list)
            authors = dict(zip(it, it))
            for name in authors:
                authors[name] = authors[name]
            return authors

    def authors(self,format=None):
        result = git.shortlog("-s", "-n", _tty_in=True, _tty_out=False)
        if format == None:
            return result
        elif format == "dict":
            list = result.replace("\n", "\t").split("\t")[:-1]
            it = iter(list[::-1])
            authors = dict(zip(it, it))
            for name in authors:
                authors[name] = int(authors[name])
            return authors

    def info(self):
        authors = self.authors("dict")
        email = self.emails("dict")

        info = {}
        for name in authors:
            info[name] = {
                "name": name,
                "commits": authors[name],
                 "email": email[name]}
        return info

    def stat(self,email):
        sum= [0,0,0]
        for line in git.log("--stat", '--author={0}'.format(email), _tty_in=True, _tty_out=False, _iter=True):
            line = line[:-1]

            if " files changed" in line:
                line = line.replace(" insertions(+)","")
                line = line.replace(" insertion(+)","")
                line = line.replace(" deletion(-)","")
                line = line.replace(" deletions(-)","")
                line = line.replace(" files changed","")
                line = line.split(",")
                data = [int(i) for i in line]
                for index in range(0,len(data)):
                    sum[index] += data[index]

        return {"email": email,
               "fileschanged": sum[0],
               "inserted": sum[1],
               "deleted": sum[2],
               "lineschanged": sum[1] + sum[2],
               }

    def compute(self):
        emails = set(gitinfo.emails("dict").values())

        stats ={}
        sum = {"fileschanged":0,"inserted":0,"deleted":0,"lineschanged":0}
        for email in emails:
            print "Calculating stats for",  email
            stats[email] = gitinfo.stat(email)
    
            sum["fileschanged"] += stats[email]["fileschanged"]
            sum["inserted"] += stats[email]["inserted"]
            sum["deleted"] += stats[email]["deleted"]
            sum["lineschanged"] += stats[email]["lineschanged"]

        for email in emails:
            stats[email] = {'percentage': [
                stats[email]["fileschanged"] / float(sum["fileschanged"]),
                stats[email]["inserted"] / float(sum["inserted"]),
                stats[email]["deleted"] / float(sum["deleted"]),
                stats[email]["lineschanged"] / float(sum["lineschanged"] ),
                ]
            }

        return stats

gitinfo = GitInfo()

#print gitinfo.version()

print "A"
print gitinfo.authors()

print "b"
pprint(gitinfo.authors("dict"))

print "c"
pprint(gitinfo.emails())

print "d"
pprint(gitinfo.emails("dict"))

print "e"
pprint(gitinfo.info())

print "f"
print gitinfo.stat("laszewski@gmail.com")

print "g"
stats = gitinfo.compute()

print stats

print "h"
for email in stats:
    p = stats[email]["percentage"]
    print "{0} {1:.3f}% {2:.3f}%  {3:.3f}% {4:.3f}%".format(email, p[0], p[1], p[2], p[3])

