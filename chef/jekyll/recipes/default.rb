include_recipe 'ruby'

bash 'install rdiscount' do
    creates "/usr/local/rvm/gems/ruby-#{node[:ruby]}/bin/rdiscount"
    code "
        source /etc/profile.d/rvm.sh
        rvm use ruby-#{node[:ruby]}
        gem install rdiscount --no-ri --no-rdoc"
end

bash 'install jekyll' do
    creates "/usr/local/rvm/gems/ruby-#{node[:ruby]}/bin/jekyll"
    code "
        source /etc/profile.d/rvm.sh
        rvm use ruby-#{node[:ruby]}
        gem install jekyll --no-ri --no-rdoc"
end
