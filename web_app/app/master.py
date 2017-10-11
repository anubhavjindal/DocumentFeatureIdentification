import os
from app.config import ALLOWED_EXTENSIONS
from flask import render_template, request, redirect, send_file
from werkzeug import secure_filename
import shutil
import zipfile
import time
from flask import make_response
from os import listdir
from os.path import isfile, join
from app import app

class UserActions():
    final_classified={}

    def allowed_file(self,filename):
            return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def upload_file(self):
        if request.method == 'POST':
            files = request.files.getlist('file[]')
            responses={}
            for file in files:
                responses.update(self.handle_file(file))
            return render_template('upload.html',responses=responses,user=self)
        return render_template('upload.html',user=self)

    def handle_file(self,file):
        folder = app.config['UPLOAD_FOLDER']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            response={filename: 1}
            return response
        else:
            response={file.filename: 0}
            return response

    def fetch_files(self):
        folder = app.config['UPLOAD_FOLDER']
        allfiles = [f for f in listdir(folder) if isfile(join(folder, f)) if not f.startswith('.')]
        if allfiles:
            return allfiles

    def delete_file(self,filename):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/home/')

    def show_output(self,final):
        self.final_classified=final
        return render_template('final.html',final=self.final_classified)

    def zipper(self):
        dpath=app.config['DOWNLOAD_FOLDER']
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        zfname = 'classified-' + str(timestamp) + '.zip'
        zf = zipfile.ZipFile(dpath+zfname, mode='w')
        self.zip_dir(app.config['CAT_FOLDER'], zf)
        zf.close()
        filepath=os.path.join('files/downloads',zfname)
        return send_file(filepath, mimetype='application/zip', as_attachment=True)

    def zip_dir(self,path,ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    def download_zip(self):
        final_dict=self.final_classified
        if bool(final_dict):
            for x in final_dict.keys():
                filename=os.path.join(app.config['UPLOAD_FOLDER'], x)
                catpath=os.path.join(app.config['CAT_FOLDER'],final_dict[x])
                if not os.path.exists(catpath):
                    os.makedirs(catpath)
                shutil.move(filename,catpath)
            self.zipper()
        return redirect('/')

    def reset(self):
        folders = [app.config['UPLOAD_FOLDER'],app.config['CAT_FOLDER']]
        for folder in folders:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        return render_template('main.html')