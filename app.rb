require 'sinatra'
require './gitjekyllpreview'
require 'uri'

 
get '/' do

  "something"
end

get '/:repo/:ref/?*' do

  req_path = request.path
  
  file_path = req_path.sub("/#{params[:repo]}/#{params[:ref]}/", "")
  path = GitJekyllPreview.make_path(params[:repo], params[:ref], false)



  #http://localhost:9292/beyondtransparency/HEAD/index.html

  if !File.directory?(path)

    puts "Not found... checkout and build"
    GitJekyllPreview.checkout(params[:repo], params[:ref])
    GitJekyllPreview.build(params[:repo], params[:ref])
  end

  puts "#{params[:repo]} #{params[:ref]} #{request.path} #{file_path}"
  
  send_file "#{path}/_site/#{file_path}"


end
 

