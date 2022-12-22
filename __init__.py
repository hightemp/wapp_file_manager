from flask import g, Flask, render_template, request, send_file, redirect, session, jsonify
import os
import re
import sqlite3
import re
import base64
import urllib.parse
from flask import Response

import mimetypes
# from static_packed import dFiles
# import io

app = Flask(__name__)

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

# @app.route("/static_dyn/<path:path>", methods=['GET', 'POST'])
# def static_dyn(path):
#     path = "./static/"+path
#     # sContentType = request.headers['Accept'].split(',')[0]
#     sContentType = mimetypes.guess_type(path)[1]
#     print(sContentType)
#     sBaseName = os.path.basename(path)
#     # response = make_response(image_binary)
#     # response.headers.set('Content-Type', 'image/jpeg')
#     # return dFiles[path]
#     return send_file(
#         io.BytesIO(bytearray(dFiles[path])),
#         download_name=sBaseName,
#         mimetype=sContentType
# )

@app.route("/", methods=['GET', 'POST'])
def index():
    if (request.args.get('init_db', '')=='1'):
        print("=========================================================")
        print("INIT DB")
        init_db()
        print("=========================================================")
        return redirect("/")

    sBaseURL = request.url

    from os import listdir
    from os.path import isdir, isfile, join

    sSelected = request.args.get('sSelected', '')
    sPath = request.args.get('sPath', '')
    sDir = request.args.get('sDir', '')
    sFile = request.args.get('sFile', '')
    sFileExt = request.args.get('sFileExt', 'Все')

    print("[>]", request.args)
    if ("action" in request.args):
        if request.args["action"]=="create_dir":
            return render_template('dir_create.html', 
                sSelected=sSelected
            )
        if request.args["action"]=="remove_dir":
            return render_template('dir_remove.html', 
                sSelected=sSelected
            )
        if request.args["action"]=="clean_dirs":
            return render_template('dir_clean.html', 
                sSelected=sSelected
            )
        if request.args["action"]=="copy_dir":
            return ""
        if request.args["action"]=="accept_save_dir":
            os.mkdir(request.args["name"])
        if request.args["action"]=="accept_remove_dir":
            aDirs = request.args.getlist("dirs[]")
            for sDir in aDirs:
                os.rmdir(os.path.join(sPath, sDir))
        if request.args["action"]=="accept_clean_dirs":
            pass

        if request.args["action"]=="create_file":
            return render_template('file_create.html', 
                sSelected=sSelected
            )
        if request.args["action"]=="remove_file":
            aFiles = request.args.getlist("files[]")
            return render_template('file_remove.html', 
                aFiles=aFiles,
                sSelected=sSelected,
                sPath=sPath,
                sDir=sDir,
                sFile=sFile                
            )
        if request.args["action"]=="clean_files":
            return render_template('file_clean.html', 
                sSelected=sSelected
            )
        if request.args["action"]=="copy_file":
            aFiles = request.args.getlist("files[]")
            return ""
        if request.args["action"]=="accept_save_file":
            pass
        if request.args["action"]=="accept_remove_file":
            aFiles = request.args.getlist("files[]")
            for sFile in aFiles:
                print(os.path.join(sPath, sFile))
                os.unlink(os.path.join(sPath, sFile))
        if request.args["action"]=="accept_clean_files":
            pass

        if request.args["action"]=="upload_files":
            return render_template('upload_files.html')
        if request.args["action"]=="download_files":
            aFiles = request.args.getlist("files[]")
            return render_template('download_files.html',
                aFiles=aFiles,
                sSelected=sSelected,
                sPath=sPath,
                sDir=sDir,
                sFile=sFile
            )

        return redirect(request.path+"?sSelected="+sSelected)
    
    sPreviewURL="about:blank"

    if sFile != '':
        sPreviewURL = "preview?sSelected="+sSelected+"&sFile="+sFile
        print('[!] FILE SAVED:'+sFile)
        get_db().execute("UPDATE tabs SET selected_file=? WHERE id=?", (sFile, sSelected))
        get_db().commit()
    else:
        aCurTab = query_db('SELECT * FROM tabs WHERE id=? LIMIT 1', (sSelected,))
        if len(aCurTab)>0 and len(aCurTab[0])>3:
            sFile = aCurTab[0][3]
            if sFile:
                sPreviewURL = "preview?sSelected="+sSelected+"&sFile="+sFile

    aFiles = []
    aDirs = []
    aFilesInfo = []
    oGroupedFiles = dict()

    if sPath != '':
        print('[!] SAVED:'+sPath)
        get_db().execute("UPDATE tabs SET path=? WHERE id=?", (sPath, sSelected))
        get_db().commit()
    
    aTabs = query_db('SELECT * FROM tabs')
    aExitstsTabs = [os.path.isdir(f[2]) for f in aTabs]
    # print(aTabs)

    aCurTab = query_db('SELECT * FROM tabs WHERE id=? LIMIT 1', (sSelected,))
    if len(aCurTab)>0 and len(aCurTab[0])>1:
        sPath = aCurTab[0][2]

    print("[!] PATH 1:"+sPath+", "+sDir)
    if sDir:
        sPath = os.path.realpath(os.path.join(sPath, sDir))
        print("[!] PATH 2:"+sPath+", "+sDir)
        get_db().execute("UPDATE tabs SET path=? WHERE id=?", (sPath, sSelected))
        get_db().commit()
        return redirect(request.path+"?sSelected="+sSelected)
    print("[!] PATH 2:"+sPath+", "+sDir)

    try:
        if sPath!='' and os.path.isdir(sPath):
            aFiles = sorted([f for f in listdir(sPath) if isfile(join(sPath, f))])
            aDirs = sorted([f for f in listdir(sPath) if isdir(join(sPath, f))])

            # NOTE: Группировка файлов по расширениям
            oGroupedFiles['Все'] = aFiles
            for sFileN in aFiles:
                aExt = sFileN.split('.')
                sExt = '.'
                if aExt[0] != '':
                    sExt = aExt.pop()
                if not oGroupedFiles.get(sExt, ''):
                    oGroupedFiles[sExt] = []
                oGroupedFiles[sExt].append(sFileN)

            aFiles = oGroupedFiles[sFileExt]
            aFilesInfoTemp = [os.stat(os.path.join(sPath, f)) for f in aFiles]
            aFilesInfo = []

            for iI, oI in enumerate(aFilesInfoTemp):
                aFilesInfo.append({'human_size': sizeof_fmt(oI.st_size)})
    except RuntimeError as e:
        print("[E] ERROR:"+e)
        pass

    return render_template('index.html', 
        sSelected=sSelected, 
        aTabs=aTabs, 
        sFileExt=sFileExt,
        aExitstsTabs=aExitstsTabs,
        sPath=sPath,
        aDirs=aDirs, 
        aFiles=aFiles,
        aFilesInfo=aFilesInfo,
        oGroupedFiles=oGroupedFiles,
        sCurDir=sDir,
        sCurFile=sFile,
        sPreviewURL=sPreviewURL,
        sBaseURL=sBaseURL
    )

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

@app.route("/getfile")
def getfile():
    bDownload = request.args.get('bDownload', '')
    sFullPath = request.args.get('sFullPath', '')
    print("[!] >> "+sFullPath)

    if bDownload != '1':
        if re.search(r"djvu$", sFullPath):
            sFileName = os.path.basename(sFullPath)+'.pdf'
            sTmpFile = '/tmp/'+sFileName
            print("[!] >> "+sTmpFile)
            if not os.path.isfile(sTmpFile):
                sCMD = 'ddjvu -format=pdf -quality=85 "'+sFullPath+'" "'+sTmpFile+'" '
                os.system(sCMD)
            sFullPath = sTmpFile

        if re.search(r"docx$", sFullPath):
            sFileName = os.path.basename(sFullPath)+'.pdf'
            sTmpFile = '/tmp/'+sFileName
            print("[!] >> "+sTmpFile)
            if not os.path.isfile(sTmpFile):
                sCMD = 'unoconv -f pdf -o "'+sTmpFile+'" "'+sFullPath+'"'
                os.system(sCMD)
            sFullPath = sTmpFile

    if not os.path.isfile(sFullPath):
        return "<h1>Файл не найден</h1><p>"+sFullPath+"</p>"

    resp = Response(open(sFullPath, 'rb').read())

    if re.search(r"(pdf|docx)$", sFullPath):    
        resp.headers['Content-Type'] = 'application/pdf'
    
    return resp

@app.route("/preview")
def preview():
    sSelected = request.args.get('sSelected', '')
    sFile = request.args.get('sFile', '')

    aCurTab = query_db('SELECT * FROM tabs WHERE id=? LIMIT 1', (sSelected,))
    if len(aCurTab)>0 and len(aCurTab[0])>1:
        sFullPath = aCurTab[0][2]

    sFullPath = os.path.join(sFullPath, sFile)

    if not os.path.isfile(sFullPath):
        return "<h1>Файл не найден</h1><p>"+sFullPath+"</p>" 
    
    oRegImgExt = re.compile(r"(APNG|AVIF|GIF|JPG|JPEG|PNG|SVG|BMP|ICO|TIFF)$", re.IGNORECASE)
    
    if (oRegImgExt.search(sFile)):
        print(sFullPath)
        return render_template('preview_image.html', 
            sFullPath=sFullPath,
            sFullSizeBase64Code=base64.b64encode(open(sFullPath,'rb').read()).decode('utf-8')
        )

    oRegPDFExt = re.compile(r"(PDF|DJVU|DOCX)$", re.IGNORECASE)
    
    if (oRegPDFExt.search(sFile)):
        return render_template('preview_pdf.html', 
            sFullPath="/getfile?sFullPath="+urllib.parse.quote(sFullPath)
        )
    
    if is_binary_string(open(sFullPath, 'rb').read(1024)):
        return "<h1>Бинарный файл</h1><p>"+sFullPath+"</p>" 
    else:
        sCode = open(sFullPath).read()
        return render_template('preview_textfile.html', 
            sCode=sCode
        )

@app.route("/readme")
def readme():
    sSelected = request.args.get('sSelected', '')
    # return redirect("/?sSelected="+sSelected)

@app.route("/tabs_add")
def tabs_add():
    sSelected = request.args.get('sSelected', '')

    if ("save" in request.args):
        get_db().execute(
            "INSERT INTO (title, path) VALUES (?, ?)", 
            (request.args['title'], 
            request.args['path'])
        )
        get_db().commit()
    else:
        return render_template('form_new_tab.html', 
            sSelected=sSelected
        )

    return redirect("/?sSelected="+sSelected)

@app.route("/tabs_remove")
def tabs_remove():
    sSelected = request.args.get('sSelected', '')

    if ("save" in request.args):
        get_db().execute("DELETE tabs WHERE id=?", (sSelected,))
        get_db().commit()
    else:
        return render_template('form_delete_tab.html', 
            sSelected=sSelected
        )

    return redirect("/?sSelected="+sSelected)

@app.route("/tabs_clean")
def tabs_clean():
    sSelected = request.args.get('sSelected', '')

    if ("save" in request.args):
        get_db().execute("DELETE tabs")
        get_db().commit()
    else:
        return render_template('form_clean_tab.html', 
            sSelected=sSelected
        )

    return redirect("/?sSelected="+sSelected)

import sysrsync

from apscheduler.schedulers.background import BackgroundScheduler

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=1)
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