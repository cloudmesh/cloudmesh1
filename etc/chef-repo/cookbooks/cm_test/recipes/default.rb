#
# Cookbook Name:: cm_test
# Recipe:: default
#

filename = File.expand_path('~') + '/hallo.html'

template filename do
  source 'index.html.erb'
end
