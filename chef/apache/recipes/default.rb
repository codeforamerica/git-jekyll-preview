package 'apache2'

link '/etc/apache2/mods-enabled/proxy.conf' do
    to '/etc/apache2/mods-available/proxy.conf'
    action :create
end

link '/etc/apache2/mods-enabled/proxy.load' do
    to '/etc/apache2/mods-available/proxy.load'
    action :create
end

link '/etc/apache2/mods-enabled/ssl.conf' do
    to '/etc/apache2/mods-available/ssl.conf'
    action :create
end

link '/etc/apache2/mods-enabled/ssl.load' do
    to '/etc/apache2/mods-available/ssl.load'
    action :create
end

link '/etc/apache2/mods-enabled/socache_shmcb.load' do
    to '/etc/apache2/mods-available/socache_shmcb.load'
    action :create
end

link '/etc/apache2/mods-enabled/proxy_http.load' do
    to '/etc/apache2/mods-available/proxy_http.load'
    action :create
end

link '/etc/apache2/mods-enabled/headers.load' do
    to '/etc/apache2/mods-available/headers.load'
    action :create
end

file '/etc/apache2/sites-available/jekit.conf' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content File.open(File.dirname(__FILE__) + "/apache-jekit.conf").read()
end

link '/etc/apache2/sites-enabled/000-default.conf' do
    action :delete
end

link '/etc/apache2/sites-enabled/jekit.conf' do
    to '/etc/apache2/sites-available/jekit.conf'
    action :create
end

link '/etc/apache2/sites-enabled/default-ssl.conf' do
    to '/etc/apache2/sites-available/default-ssl.conf'
    action :delete
end

file '/etc/apache2/sites-available/jekit-ssl.conf' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content File.open(File.dirname(__FILE__) + "/apache-ssl.conf").read()
end

file '/etc/ssl/certs/cfa-2014-ssl.crt' do
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

file '/etc/ssl/private/cfa-2014-ssl.key' do
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

link '/etc/apache2/sites-enabled/jekit-ssl.conf' do
    to '/etc/apache2/sites-available/jekit-ssl.conf'
    action :create
end

#
# Make it go.
#
execute "apache2ctl restart"
