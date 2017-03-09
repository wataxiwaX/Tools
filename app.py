# coding:utf-8

import web
import cgi
import time
import os
import thread
from PIL import Image
from glob import glob

web.config.debug = False

# 限制上传图片大小5MB
cgi.maxlen = 5 * 1024 * 1024

urls = (
    '/', 'index',
    '/result', 'result',
)

render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index()

    def POST(self):
        try:
            picture_convert(web.input(uploadfile = {}, targetformat = ''))
        except ValueError:
            return "图片大小超过上限(5MB)"

def picture_convert(upload):
    if upload['uploadfile'].filename:
        img = Image.open(upload['uploadfile'].file)
        filedir = 'static/'
        filepath = upload['uploadfile'].filename.replace('\\', '/')
        filename = filedir + filepath.split('/')[-1].split('.')[0] + '.' + upload['targetformat']
        img.convert('RGB').save(filename)
        raise web.seeother('/result?name=' + filename)
    else:
        raise web.seeother('/')
        
class result:
    def GET(self):
        tmp = web.input(name=None)
        urlpath = '/' + tmp.name
        filename = tmp.name.split('/')[-1]
        thread.start_new_thread(removefile, (tmp.name,))
        return render.result(urlpath, filename)

def removefile(filename):
    time.sleep(30)
    os.remove(filename)

if __name__ == "__main__":
    application = web.application(urls, globals())
    application.run()