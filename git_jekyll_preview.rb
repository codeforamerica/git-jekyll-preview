require 'sinatra'
require './preview_generator'
require 'uri'

class GitJekyllPreview < Sinatra::Base
  get '/:repo/:ref/?*' do
    req_path = request.path
    file_path = req_path.sub("/#{params[:repo]}/#{params[:ref]}/", "")
    path = PreviewGenerator.make_path(params[:repo], params[:ref], false)

    #http://localhost:9292/beyondtransparency/HEAD/index.html

    if !File.directory?(path)
      puts "Not found... checkout and build"
      PreviewGenerator.checkout(params[:repo], params[:ref])
      PreviewGenerator.build(params[:repo], params[:ref])
    end
    puts "#{params[:repo]} #{params[:ref]} #{request.path} #{file_path}"
    send_file "#{path}/_site/#{file_path}"
  end
end

