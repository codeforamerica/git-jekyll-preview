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

link '/etc/apache2/mods-enabled/proxy_http.load' do
    to '/etc/apache2/mods-available/proxy_http.load'
    action :create
end

file '/etc/apache2/sites-available/jekit' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content File.open(File.dirname(__FILE__) + "/apache-jekit.conf").read()
end

link '/etc/apache2/sites-enabled/000-default' do
    action :delete
end

link '/etc/apache2/sites-enabled/jekit' do
    to '/etc/apache2/sites-available/jekit'
    action :create
end

link '/etc/apache2/sites-enabled/default-ssl' do
    to '/etc/apache2/sites-available/default-ssl'
    action :delete
end

file '/etc/apache2/sites-available/jekit-ssl' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content File.open(File.dirname(__FILE__) + "/apache-ssl.conf").read()
end

file '/etc/ssl/certs/jekit_codeforamerica_org.crt' do
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

file '/etc/ssl/private/jekit-secret.key' do
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

link '/etc/apache2/sites-enabled/jekit-ssl' do
    to '/etc/apache2/sites-available/jekit-ssl'
    action :create
end

#
# Make it go.
#
execute "apache2ctl restart"
