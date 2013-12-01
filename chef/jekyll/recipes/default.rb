include_recipe 'ruby-2.0.0-p353'

bash 'install rdiscount' do
    not_if 'gem list -i rdiscount'
    code '
    source /etc/profile.d/rvm.sh
    /usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem install rdiscount --no-ri --no-rdoc
    '
end

bash 'install jekyll' do
    not_if 'gem list -i jekyll'
    code '
    source /etc/profile.d/rvm.sh
    /usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem install jekyll --no-ri --no-rdoc
    '
end
