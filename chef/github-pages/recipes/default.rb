package 'ruby2.0'
package 'ruby2.0-dev'
package 'zlib1g-dev'

gem_package 'github-pages' do
    gem_binary '/usr/bin/gem2.0'
    options "--no-rdoc --no-ri"
    action :install
end

# Jekyll wants a JS runtime
package 'nodejs'
