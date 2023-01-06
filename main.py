from flask import g, Flask, request, send_file, redirect, session, jsonify
from flask import session, url_for
from flask import Response

import os
import re
import re
import base64
import urllib.parse

import importlib.resources
import jinja2
from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import Flask
import mimetypes

from os import listdir
from os.path import isdir, isfile, join

from request_vars import *
from database import *
from baselib import *
import pydotenv

app = Flask(__name__)

@app.route("/zip/static/<path:path>", methods=['GET', 'POST'])
def static_dyn(path):
    oR = Response(readfile("static/"+path), mimetype=mimetypes.guess_type(path)[0])
    oR.headers['Cache-Control'] = 'max-age=60480000, stale-if-error=8640000, must-revalidate'
    return oR

@app.route("/", methods=['GET', 'POST'])
def index():
    oR = RequestVars()
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    if "create-dir" in oR.oArgs:
        return render_template('dir_create.html', oR=oR)
    if "remove-dir" in oR.oArgs:
        return render_template('dir_remove.html', oR=oR)
    if "clean-dirs" in oR.oArgs:
        return render_template('dir_clean.html', oR=oR)
    if "copy-dir" in oR.oArgs:
        return ""
    if "accept-save-dir" in oR.oArgs:
        os.mkdir(oR.oArgs["name"])
    if "accept-remove-dir" in oR.oArgs:
        oR.aDirs = oR.oArgsLists["dirs"]
        for sDir in oR.aDirs:
            os.rmdir(os.path.join(oR.sPath, sDir))
    if "accept-clean-dirs" in oR.oArgs:
        pass

    if "create-file" in oR.oArgs:
        return render_template('file_create.html', oR=oR)
    if "remove-file" in oR.oArgs:
        oR.aFiles = oR.oArgsLists["files"]
        return render_template('file_remove.html', oR=oR)
    if "clean-files" in oR.oArgs:
        return render_template('file_clean.html', oR=oR)
    if "copy-file" in oR.oArgs:
        oR.aFiles = oR.oArgsLists["files"]
        return ""
    if "accept-save-file" in oR.oArgs:
        pass
    if "accept-remove-file" in oR.oArgs:
        oR.aFiles = oR.oArgsLists["files"]
        for sFile in oR.aFiles:
            os.unlink(os.path.join(oR.sPath, sFile))
    if "accept-clean-files" in oR.oArgs:
        pass

    if "upload-files" in oR.oArgs:
        return render_template('upload_files.html')
    if "download-files" in oR.oArgs:
        oR.aFiles = oR.oArgsLists["files"]
        return render_template('download_files.html', oR=oR)

        # return redirect(request.path+"?select-tab="+sSelected)
    
    oR.sPreviewURL="about:blank"

    if oR.sFile != '':
        oR.sPreviewURL = "preview?select-tab="+oR.sSelectTab+"&file="+oR.sFile
        Tab.update({"selected_file":oR.sSelectFile}).where(Tab.id==oR.sSelectTab)
    else:
        oTab = None
        try:
            oTab = Tab.select().where(Tab.id==oR.sSelectTab).get()
        except:
            oTab = None
        if oTab:
            oR.sPreviewURL = "preview?select-tab="+oR.sSelectTab+"&file="+oTab.selected_file

    if oR.sSelectPath != '':
        print('[!] SAVED:'+oR.sSelectPath)
        Tab.update({"path":oR.sSelectPath}).where(Tab.id==oR.sSelectTab)
    
    oR.aTabs = Tab.select()
    oR.aExitstsTabs = [os.path.exists(f.path) for f in oR.aTabs]

    oR.oCurTab = None
    try:
        oR.oCurTab = Tab.select().where(Tab.id==oR.sSelectTab).get()
    except:
        oR.oCurTab = None
    if oR.oCurTab:
        oR.sPath = oR.oCurTab.path

    print(request.url)
    print("[!] PATH 1:"+oR.sPath+", "+oR.sDir)
    if oR.sDir:
        oR.sPath = os.path.realpath(os.path.join(oR.sPath, oR.sDir))
        print("[!] PATH 2:"+oR.sPath+", "+oR.sDir)
        Tab.update({"path":oR.sPath}).where(Tab.id==oR.sSelectTab).execute()
        del oR.oArgs["dir"]
        return redirect(url_for('.index', **oR.oArgs))
    print("[!] PATH 2:"+oR.sPath+", "+oR.sDir)

    try:
        if oR.sPath!='' and os.path.isdir(oR.sPath):
            oR.aFiles = sorted([f for f in listdir(oR.sPath) if isfile(join(oR.sPath, f))])
            oR.aDirs = sorted([f for f in listdir(oR.sPath) if isdir(join(oR.sPath, f))])

            # NOTE: Группировка файлов по расширениям
            oR.oGroupedFiles['Все'] = oR.aFiles
            for sFileN in oR.aFiles:
                aExt = sFileN.split('.')
                sExt = '.'
                if aExt[0] != '':
                    sExt = aExt.pop()
                if not oR.oGroupedFiles.get(sExt, ''):
                    oR.oGroupedFiles[sExt] = []
                oR.oGroupedFiles[sExt].append(sFileN)

            if oR.sFileExt == '':
                oR.sFileExt = 'Все'
            if not oR.sFileExt in oR.oGroupedFiles:
                oR.sFileExt = 'Все'
            oR.aFiles = oR.oGroupedFiles[oR.sFileExt]
            oR.aFilesInfoTemp = [os.stat(os.path.join(oR.sPath, f)) for f in oR.aFiles]
            oR.aFilesInfo = []

            for iI, oI in enumerate(oR.aFilesInfoTemp):
                oR.aFilesInfo.append({'human_size': sizeof_fmt(oI.st_size)})
    except RuntimeError as e:
        print("[E] ERROR:"+e)
        pass

    return render_template('index.html', oR=oR)

@app.route("/getfile")
def getfile():
    oR = RequestVars()
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    print("[!] >> "+oR.sFullPath)

    if oR.sDownload != '1':
        # NOTE: Превью PDF
        if re.search(r"djvu$", oR.sFullPath):
            sFileName = os.path.basename(oR.sFullPath)+'.pdf'
            sTmpFile = '/tmp/'+sFileName
            print("[!] >> "+sTmpFile)
            if not os.path.isfile(sTmpFile):
                sCMD = 'ddjvu -format=pdf -quality=85 "'+oR.sFullPath+'" "'+sTmpFile+'" '
                os.system(sCMD)
            oR.sFullPath = sTmpFile
        # NOTE: Превью DOCX
        if re.search(r"docx$", oR.sFullPath):
            sFileName = os.path.basename(oR.sFullPath)+'.pdf'
            sTmpFile = '/tmp/'+sFileName
            print("[!] >> "+sTmpFile)
            if not os.path.isfile(sTmpFile):
                sCMD = 'unoconv -f pdf -o "'+sTmpFile+'" "'+oR.sFullPath+'"'
                os.system(sCMD)
            oR.sFullPath = sTmpFile

    if not os.path.isfile(oR.sFullPath):
        return "<h1>Файл не найден</h1><p>"+oR.sFullPath+"</p>"

    resp = Response(open(oR.sFullPath, 'rb').read())

    if re.search(r"(pdf|docx)$", oR.sFullPath):    
        resp.headers['Content-Type'] = 'application/pdf'
    
    return resp

@app.route("/preview")
def preview():
    oR = RequestVars()
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    # sSelected = request.args.get('sSelected', '')
    # sFile = request.args.get('sFile', '')

    oR.oCurTab = None
    try:
        oR.oCurTab = Tab.select().where(Tab.id==oR.sSelectTab).get()
    except:
        oR.oCurTab = None
    if oR.oCurTab:
        oR.sFullPath = oR.oCurTab.path

    if oR.sFile == "":
        return "" 
    
    oR.sFullPath = os.path.join(oR.sFullPath, oR.sFile)

    if not os.path.isfile(oR.sFullPath):
        return "<h1>Файл не найден</h1><p>"+oR.sFullPath+"</p>" 
    
    # NOTE: Превью для изображений
    oRegImgExt = re.compile(r"(APNG|AVIF|GIF|JPG|JPEG|PNG|SVG|BMP|ICO|TIFF)$", re.IGNORECASE)
    if (oRegImgExt.search(oR.sFile)):
        print(oR.sFullPath)
        return render_template('preview_image.html', 
            sFullPath=oR.sFullPath,
            sFullSizeBase64Code=base64.b64encode(open(oR.sFullPath,'rb').read()).decode('utf-8')
        )

    # NOTE: Превью для документов
    oRegPDFExt = re.compile(r"(PDF|DJVU|DOCX)$", re.IGNORECASE)
    if (oRegPDFExt.search(oR.sFile)):
        return render_template('preview_pdf.html', 
            sFullPath=urllib.parse.quote("/getfile?full-path="+oR.sFullPath)
        )
    
    if is_binary_string(open(oR.sFullPath, 'rb').read(1024)):
        return "<h1>Бинарный файл</h1><p>"+oR.sFullPath+"</p>" 
    else:
        sCode = open(oR.sFullPath).read()
        return render_template('preview_textfile.html', 
            sCode=sCode
        )

@app.route("/readme")
def readme():
    pass

# @app.route("/tabs_add")
# def tabs_add():
#     sSelected = request.args.get('sSelected', '')

#     if ("save" in request.args):
#         get_db().execute(
#             "INSERT INTO (title, path) VALUES (?, ?)", 
#             (request.args['title'], 
#             request.args['path'])
#         )
#         get_db().commit()
#     else:
#         return render_template('form_new_tab.html', 
#             sSelected=sSelected
#         )

#     return redirect("/?sSelected="+sSelected)

# @app.route("/tabs_remove")
# def tabs_remove():
#     sSelected = request.args.get('sSelected', '')

#     if ("save" in request.args):
#         get_db().execute("DELETE tabs WHERE id=?", (sSelected,))
#         get_db().commit()
#     else:
#         return render_template('form_delete_tab.html', 
#             sSelected=sSelected
#         )

#     return redirect("/?sSelected="+sSelected)

# @app.route("/tabs_clean")
# def tabs_clean():
#     sSelected = request.args.get('sSelected', '')

#     if ("save" in request.args):
#         get_db().execute("DELETE tabs")
#         get_db().commit()
#     else:
#         return render_template('form_clean_tab.html', 
#             sSelected=sSelected
#         )

#     return redirect("/?sSelected="+sSelected)

import sysrsync

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

def fnShedulerJob():
    pass

sched = BackgroundScheduler(daemon=True)
sched.add_job(fnShedulerJob, IntervalTrigger(), minutes=1)
sched.start()

@app.route("/find")
def find():

    if ("action" in request.args):
        if request.args["action"]=="find_add":
            pass
        if request.args["action"]=="find_edit":
            pass
        if request.args["action"]=="find_remove":
            pass
    
    return render_template('find.html')

@app.route("/mounts")
def mounts():
    
    if ("action" in request.args):
        if request.args["action"]=="mounts_add":
            pass
        if request.args["action"]=="mounts_edit":
            pass
        if request.args["action"]=="mounts_remove":
            pass
    
    return render_template('mounts.html')

@app.route("/rsync")
def rsync():
    
    if ("action" in request.args):
        if request.args["action"]=="rsync_add":
            pass

        if request.args["action"]=="rsync_edit":
            pass

        if request.args["action"]=="rsync_remove":
            pass

        if request.args["action"]=="rsync_option_add":
            pass

        if request.args["action"]=="rsync_option_edit":
            pass

        if request.args["action"]=="rsync_option_remove":
            pass

        if request.args["action"]=="rsync_process_add":
            pass

        if request.args["action"]=="rsync_process_edit":
            pass

        if request.args["action"]=="rsync_process_remove":
            pass
            # get_db().execute("DELETE tabs WHERE id=?", (sSelected,))
            # get_db().commit()

    return render_template('rsync_list.html')

@app.route("/favorites", methods=['GET', 'POST'])
def favorites():
    return render_template('favorites.html')

def run():
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    run()