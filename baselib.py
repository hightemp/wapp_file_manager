from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import render_template as render_template_default
from peewee import *
from playhouse.shortcuts import model_to_dict
import os
import zipfile
from database import *
from flask import g, Flask, request
import pkgutil
import yaml
import sys

__DEBUG__ = False
__PYINST__ = False

YAML_FILE = './config.yaml'

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

def fnLoadConfigDirs():
    if not os.path.isfile(YAML_FILE):
        sHome = os.path.expanduser("~")
        return {"tabs":{"root": "/", "home": sHome}}
    with open(YAML_FILE, "r") as f:
        return yaml.load(f.read())

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def fnIsPyInstaller():
    return getattr(sys, 'frozen', False)

def readfile(sFilePath):
    if (__DEBUG__):
        return open(sFilePath, 'rb').read()
    elif (__PYINST__ or fnIsPyInstaller()):
        print(sFilePath)
        return pkgutil.get_data('main', sFilePath )
    else:
        with zipfile.ZipFile(os.path.dirname(__file__)) as z:
            # print(z.namelist())
            with z.open(sFilePath) as f:
                print("[!] "+f.name)
                # print("[!] "+f.read().decode("utf-8"))
                return f.read()
        return "ERROR"

def load_template(name):
    return readfile("templates/"+name).decode("utf-8")

oTempFunctionLoader = FunctionLoader(load_template)

def render_template(name, **kwargs):
    if __DEBUG__:
        return render_template_default(name, **kwargs)
    else:
        data = load_template(name)
        tpl = Environment(loader=oTempFunctionLoader).from_string(data)
        return tpl.render(**kwargs)

def models_col_to_list(lModelsCol):
    lList = []
    for oA in lModelsCol:
        lList.append(model_to_dict(oA))

    return lList

# NOTE: ??????????????
def parse_get(args):
    data = {}

    for u, v in args.lists():
        if hasattr(v, "__len__"):
            for k in v:
                data[u] = k
                if k == '':
                    del data[u]
        else:
            data[u] = v
            if v == '':
                del data[u]

    return data

def parse_multi_form(form):
    data = {}
    for url_k, v in form.lists():
        if ('' in v):
            continue
        v = v[0]

        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data

def fnPrepareFormFields(aFields, cCls, sSelID):
    if isinstance(cCls, str):
        kls = globals()[cCls]
    else:
        kls = cCls
    oItem = {}
    if sSelID != "" and int(sSelID) > 0:
        try:
            oItem = kls.get_by_id(sSelID)
            oItem = model_to_dict(oItem, recurse=False, backrefs=False)
        except:
            pass

    for sK, oV in aFields.items():
        if 'sel_value' in aFields[sK]:
            aFields[sK]['value'] = aFields[sK]['sel_value']
        else:
            if sSelID==0:
                aFields[sK]['value'] = ''
            else:
                if sK in oItem and oItem[sK]:
                    aFields[sK]['value'] = oItem[oV['field_name']]
                else:
                    aFields[sK]['value'] = ''
    return aFields

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return 's'+''.join(x.title() for x in components[0:])

def fnPrepareArgs(oR):
    oR.sBaseURL = request.url
    oR.sPathURL = request.path

    oR.oArgs = parse_get(request.args)
    oR.oArgsLists = parse_multi_form(request.args)

    print(oR.oArgs)
    print(oR.oArgsLists)

    for sK in oR.oArgs:
        sVarName = to_camel_case(sK)
        setattr(oR, sVarName, oR.oArgs[sK])

def fnPrepareFormArgs(oR, sName):
    oR.oArgs = parse_get(request.args)
    oR.oArgsLists = parse_multi_form(request.args)

    for sK in oR.oArgs:
        # sVarName = to_camel_case(sK)
        sVarName = ""
        setattr(oR, sVarName, oR.oArgs[sK])

def models_col_to_list(lModelsCol):
    lList = []
    for oA in lModelsCol:
        lList.append(model_to_dict(oA))

    return lList

def fnPrepareFormFields(aFields, oKls, sSelID):
    oItem = {}
    if sSelID != "" and int(sSelID) > 0:
        try:
            oItem = oKls.get_by_id(sSelID)
            oItem = model_to_dict(oItem, recurse=False, backrefs=False)
        except:
            pass

    for sK, oV in aFields.items():
        if 'sel_value' in aFields[sK]:
            aFields[sK]['value'] = aFields[sK]['sel_value']
        else:
            if sSelID==0:
                aFields[sK]['value'] = ''
            else:
                if (sK in oItem and oItem[sK]) or (oV['field_name'] in oItem):
                    print("[+]", sK, oV['field_name'], oItem[oV['field_name']])
                    aFields[sK]['value'] = oItem[oV['field_name']]
                else:
                    # print("[-]", sK, oV['field_name'], oItem[oV['field_name']])
                    aFields[sK]['value'] = ''
    return aFields

def fnIsFile(sFullPath):
    return os.path.isfile(os.path.expanduser(sFullPath))

def fnReadFile(sFullPath):
    return open(os.path.expanduser(sFullPath), 'rb').read()