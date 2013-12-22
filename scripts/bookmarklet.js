var href = location.href,
    url = false;

if(href.match(/^https:\/\/github.com\/.+\/.+\/(edit|blob)\//))
{
    if(href.match(/^.+\/_posts\/....-..-..-.+$/))
    {
        var url = href.replace(/^.+\/(.+\/.+)\/(edit|blob)\/(.+)\/_posts\/(....)-(..)-(..)-(.+)$/,
                               'http://host:port/$1/$3/$4/$5/$6/$7');
    }
    else
    {
        var url = href.replace(/^.+\/(.+\/.+)\/(edit|blob)\/([^\/]+\/.+)$/,
                               'http://host:port/$1/$3');
    }
}
else if(href.match(/^http:\/\/prose.io\/#.+\/.+\/edit\//))
{
    if(href.match(/^.+\/_posts\/....-..-..-.+$/))
    {
        var url = href.replace(/^.+\/#(.+\/.+)\/edit\/(.+)\/_posts\/(....)-(..)-(..)-(.+)$/,
                               'http://host:port/$1/$2/$3/$4/$5/$6');
    }
    else
    {
        var url = href.replace(/^.+\/#(.+\/.+)\/edit\/([^\/]+\/.+)$/,
                               'http://host:port/$1/$2');
    }
}

if(url)
{
    if(url && url.match(/\.(md|markdown)$/)) {
        url = url.replace(/\.(md|markdown)$/, '.html');
    }

    window.open(url);
}
else
{
    alert("Jekit doesn't understand this URL:\n" + href);
}
