#require 'jekyll'
require 'fileutils'



module GitJekyllPreview


  def GitJekyllPreview.make_path(repo, ref, create =true)
    path = "checkouts/#{repo}/#{ref}"
    # create the dir if needed

    if !File.directory?(path) and create
      FileUtils.mkdir_p path
    end

    path
  end

  def fetchRepo(repo)
    # make sure the repo is up to date
    system "cd repos/#{repo}; git fetch"
  end

  def GitJekyllPreview.checkout(repo, ref)

    # checkout the specified ref
    path = make_path(repo, ref)
    puts path
    system "cd repos/#{repo}; git --work-tree=../../#{path} checkout #{ref} -- ."
  end

  def GitJekyllPreview.build(repo, ref)

    # build the site.
    path = make_path(repo, ref)

    system "cd #{path}; jekyll build"

  end




  def injectBaseTag(html)
    #heh

  end



end
