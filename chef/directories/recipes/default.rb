base_dir = File.join(File.dirname(__FILE__), '..', '..', '..')

directory File.join(base_dir, 'repos') do
    mode 0777
    action :create
end

directory File.join(base_dir, 'checkouts') do
    mode 0777
    action :create
end
