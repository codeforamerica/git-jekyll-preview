package 'python-pip'

bash 'install python-flask' do
    not_if 'python -c "import flask"'
    code 'pip install flask'
end
