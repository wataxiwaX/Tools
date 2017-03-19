# coding:utf-8

import web
import cgi
import time
import os
import thread
import filetype
from PIL import Image
from glob import glob

web.config.debug = False

# 限制上传图片大小10MB
cgi.maxlen = 10 * 1024 * 1024

urls = (
    '/', 'index',
    '/picture', 'picture',
)

render = web.template.render('templates/')

class index:
    def GET(self):
        return render.index()

class picture:
    def GET(self):
        return render.picture()
        
    def POST(self):
        try:
            return picture_convert(web.input(uploadfile = {}, targetformat = ''))
        except ValueError:
            return 'too_big'

# 图片格式转换
def picture_convert(upload):
    if upload['uploadfile'].filename:
        if filetype.check_filetype(upload['uploadfile'].file, 'picture'):
            img = Image.open(upload['uploadfile'].file)
            filedir = 'static/'
            filepath = upload['uploadfile'].filename.replace('\\', '/')
            filename = filedir + filepath.split('/')[-1].split('.')[0] + '.' + upload['targetformat']
            img.convert('RGB').save(filename)
            thread.start_new_thread(removefile, (filename,))
            return 'ok', filename
        else:
            return 'not_picture'
    else:
        return 'no_file'

# 删除上传的文件
def removefile(filename):
    time.sleep(30)
    os.remove(filename)

if __name__ == "__main__":
    application = web.application(urls, globals())
    application.run()