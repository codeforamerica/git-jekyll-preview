package 'curl'

bash 'install rvm' do
    creates '/usr/local/rvm/bin/rvm'
    code 'curl -L https://get.rvm.io | bash'
end
