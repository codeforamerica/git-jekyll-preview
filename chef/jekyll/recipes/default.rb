include_recipe 'ruby-2.0.0-p353'

bash 'install github-pages' do
    not_if 'gem list -i github-pages'
    code '
    source /etc/profile.d/rvm.sh
    /usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem install github-pages --no-ri --no-rdoc
    '
end
