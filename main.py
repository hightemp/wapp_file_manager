from flask import g, Flask, render_template, request, send_file, redirect, session, jsonify
from werkzeug.utils import secure_filename
from hurry.filesize import size
from datetime import datetime
from flask_fontawesome import FontAwesome
from flask_qrcode import QRcode
from pathlib import Path
import os
import mimetypes
import sys
import re
import json
import zipfile
import filetype
import sqlite3
import glob
import re

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

@app.route("/")
def index():
    if (request.args.get('init_db', '')=='1'):
        init_db()
        return redirect("/")

    from os import listdir
    from os.path import isdir, isfile, join

    sSelected = request.args.get('sSelected', '')
    sPath = request.args.get('sPath', '')
    sDir = request.args.get('sDir', '')
    sFile = request.args.get('sFile', '')

    aFiles = []
    aDirs = []

    if sPath != '':
        print('[!] SAVED:'+sPath)
        get_db().execute("UPDATE tabs SET path=? WHERE id=?", (sPath, sSelected))
        get_db().commit()
    
    aTabs = query_db('SELECT * FROM tabs')
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
        aFiles = sorted([f for f in listdir(sPath) if isfile(join(sPath, f))])
        aDirs = sorted([f for f in listdir(sPath) if isdir(join(sPath, f))])
    except:
        pass

    return render_template('index.html', 
        sSelected=sSelected, aTabs=aTabs, 
        sPath=sPath,
        aDirs=aDirs, 
        aFiles=aFiles,
        sCurDir=sDir,
        sCurFile=sFile
    )

@app.route("/preview")
def tabs_add():
    sSelected = request.args.get('sSelected', '')
    sFile = request.args.get('sFile', '')

    aCurTab = query_db('SELECT * FROM tabs WHERE id=? LIMIT 1', (sSelected,))
    if len(aCurTab)>0 and len(aCurTab[0])>1:
        sFullPath = aCurTab[0][2]

    sFullPath = os.oath.join(sFullPath, sFile)

    oRegImgExt = re.compile("(APNG|AVIF|GIF|JPEG|PNG|SVG|BMP|ICO|TIFF)$", re.I)
    
    if (oRegImgExt.match(sFile)):
        return render_template('preview_image.html', 
            sFullPath=sFullPath
        )

    oRegImgExt = re.compile("(APNG|AVIF|GIF|JPEG|PNG|SVG|BMP|ICO|TIFF)$", re.I)
    
    if (oRegImgExt.match(sFile)):
        return render_template('preview_image.html', 
            sFullPath=sFullPath
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