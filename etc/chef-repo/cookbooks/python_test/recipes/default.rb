#
# Cookbook Name:: python_test
# Recipe:: default
#
# Copyright (c) 2014 The Authors, All Rights Reserved.
#
# Cookbook Name:: script_test
# Recipe:: default
#

results = "/tmp/output.txt"
cmd = "ls"

file results do
    action :delete
end

filename = "test.py"
 
execute 'execute_file' do
 cwd '/Users/flat/github/cloudmesh/cloudmesh/etc/chef-repo/cookbooks/python_test'
 command "python #{filename}"
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

