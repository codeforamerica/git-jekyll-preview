package 'python-pip'

bash 'install python-requests' do
    not_if 'python -c "from requests import get"'
    code 'pip install requests'
end

bash 'install python-requests-oauthlib' do
    not_if 'python -c "from requests_oauthlib import OAuth2Session"'
    code 'pip install requests-oauthlib'
end
