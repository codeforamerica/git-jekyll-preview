include_recipe 'rvm'

bash 'install ruby 2.0.0-p353' do
    creates '/usr/local/rvm/rubies/ruby-2.0.0-p353/bin/gem'
    code '/usr/local/rvm/bin/rvm install 2.0.0-p353'
end
