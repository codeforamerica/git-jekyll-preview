include_recipe 'rvm'

bash 'install ruby' do
    creates "/usr/local/rvm/rubies/ruby-#{node[:ruby]}/bin/gem"
    code "/usr/local/rvm/bin/rvm install #{node[:ruby]}"
end
