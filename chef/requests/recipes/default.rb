package 'python-pip'

bash 'install python-requests' do
    not_if 'python -c "from requests import get"'
    code 'pip install requests'
end
