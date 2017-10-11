from flask import redirect
import os
from .master import UserActions
from app import app
from classify import *

@app.route('/')
def start():
    global user
    user=UserActions()
    return user.reset()

@app.route('/home/', methods=['GET', 'POST'])
def main():
    global user
    user=UserActions()
    return user.upload_file()

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    #user=UserActions()
    return user.delete_file(filename)

@app.route('/classify/', methods=['POST'])
def classify():
    #user=UserActions()
    myfiles=user.fetch_files()
    classified={}
    corp_dict = load_dict()
    for file in myfiles:
        filepath=os.path.join(app.config['UPLOAD_FOLDER'], file)
        cfolder=classify_file(filepath, corp_dict)
        classified.update({file:cfolder})
    return user.show_output(classified)

@app.route('/getzip/', methods=['POST'])
def getzip():
    return user.download_zip()
