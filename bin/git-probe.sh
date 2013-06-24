git log --stat --author $(git config --get user.email)  | awk -F',' '/files? changed/ {
    files += $1
    insertions += $2
    deletions += $3
    print
}
END {
    print "Files Changed: " files
    print "Insertions: " insertions
    print "Deletions: " deletions
    print "Lines changed: " insertions + deletions

}'