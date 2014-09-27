link '/opt/git-jekyll-preview' do
    to File.absolute_path(File.join(File.dirname(__FILE__), '..', '..', '..'))
end

directory '/opt/git-jekyll-preview/repos' do
    mode 0777
    action :create
end

directory '/opt/git-jekyll-preview/checkouts' do
    mode 0777
    action :create
end

directory '/var/log/jekit' do
    owner 'www-data'
    group 'www-data'
    mode '0775'
    action :create
end

file '/var/log/jekit/cull-dirs.log' do
    owner 'www-data'
    group 'www-data'
    mode '0644'
    action :create
end

file '/etc/cron.hourly/cull-dirs' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content <<-cron
#!/bin/sh
cd /opt/git-jekyll-preview
sudo -u www-data python cull-dirs.py checkouts repos >> /var/log/jekit/cull-dirs.log
cron
end

file '/etc/logrotate.d/cull-dirs' do
    owner 'root'
    group 'root'
    mode '0755'
    action :create
    content <<-conf
/var/log/jekit/cull-dirs.log
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
