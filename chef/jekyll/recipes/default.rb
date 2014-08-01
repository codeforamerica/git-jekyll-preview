include_recipe 'ruby-2.0.0-p353'

bash 'install rdiscount' do
    creates '/usr/local/rvm/gems/ruby-2.0.0-p353/bin/rdiscount'
    code '
        source /etc/profile.d/rvm.sh
        rvm use ruby-2.0.0-p353
        gem install rdiscount --no-ri --no-rdoc'
end

bash 'install jekyll' do
    creates '/usr/local/rvm/gems/ruby-2.0.0-p353/bin/jekyll'
    code '
        source /etc/profile.d/rvm.sh
        rvm use ruby-2.0.0-p353
        gem install jekyll --no-ri --no-rdoc'
end
