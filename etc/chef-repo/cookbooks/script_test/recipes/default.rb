#
# Cookbook Name:: script_test
# Recipe:: default
#

results = "/tmp/output.txt"
cmd = "ls"

file results do
    action :delete
end

bash cmd do
    code <<-EOH
    echo "===========================================" > #{results}
    pwd >> #{results}
    echo "===========================================" >> #{results}
    #{cmd} >> #{results}
    echo "===========================================" >> #{results}
    EOH
end

ruby_block "Results" do
    only_if { ::File.exists?(results) }
    block do
        print "\n"
        File.open(results).each do |line|
            print line
        end
    end
end

file results do
    action :delete
end

