package 'apache2'

link '/etc/apache2/mods-enabled/proxy.conf' do
    to '/etc/apache2/mods-available/proxy.conf'
    action :create
end

link '/etc/apache2/mods-enabled/proxy.load' do
    to '/etc/apache2/mods-available/proxy.load'
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
    content <<-conf
<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www

    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>

    <Directory /var/www/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Order allow,deny
        allow from all
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/

    <Directory "/usr/lib/cgi-bin">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog ${APACHE_LOG_DIR}/access.log combined

    Alias /doc/ "/usr/share/doc/"

    <Directory "/usr/share/doc/">
        Options Indexes MultiViews FollowSymLinks
        AllowOverride None
        Order deny,allow
        Deny from all
        Allow from 127.0.0.0/255.0.0.0 ::1/128
    </Directory>

    <Location />
        ProxyPass http://127.0.0.1:8080/
        ProxyPassReverse http://127.0.0.1:8080/
    </Location>

    <Proxy http://127.0.0.1:8080/*>
        Allow from all
    </Proxy>

</VirtualHost>
conf
end

link '/etc/apache2/sites-enabled/000-default' do
    action :delete
end

link '/etc/apache2/sites-enabled/jekit' do
    to '/etc/apache2/sites-available/jekit'
    action :create
end

#
# Make it go.
#
execute "apache2ctl restart"
