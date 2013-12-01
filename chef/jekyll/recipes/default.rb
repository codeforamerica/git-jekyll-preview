include_recipe 'ruby-2.0.0-p353'

bash 'install jekyll' do
    creates '/usr/local/bin/jekyll'
    code '
    source /etc/profile.d/rvm.sh
    /usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem install rdiscount --no-ri --no-rdoc
    /usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem install jekyll --no-ri --no-rdoc
    '
end
