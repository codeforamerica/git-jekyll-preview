package 'python-pip'

bash 'install python-gunicorn' do
    not_if 'python -c "import gunicorn"'
    code 'pip install gunicorn'
end

directory '/var/log/jekit' do
    owner 'www-data'
    group 'www-data'
    mode '0775'
    action :create
end

file '/etc/init/jekit.conf' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content <<-conf
description "jekit"

start on (filesystem)
stop on runlevel [016]

respawn
console log
setuid www-data
setgid www-data
chdir /opt/git-jekyll-preview

exec /usr/local/bin/gunicorn -b 0.0.0.0:8080 -w 4 -t 300 -e app-logfile=/var/log/jekit/app.log --access-logfile /var/log/jekit/access.log make-it-so:app
conf
end

file '/etc/logrotate.d/jekit-access' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content <<-conf
/var/log/jekit/access.log
{
        copytruncate
        rotate 4
        weekly
        missingok
        notifempty
        compress
        delaycompress
        endscript
}
conf
end

file '/etc/logrotate.d/jekit-app' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content <<-conf
/var/log/jekit/app.log
{
        copytruncate
        rotate 4
        weekly
        missingok
        notifempty
        compress
        delaycompress
        endscript
}
conf
end

#
# Make it go.
#
execute "stop jekit" do
  returns [0, 1]
end

execute "start jekit"
