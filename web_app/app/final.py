import shutil
from app.config import UPLOAD_FOLDER
import zipfile

print 'creating archive'

def final_classify(final_dict):
    zf = zipfile.ZipFile('zipfile_write.zip', mode='w')
    for x in final_dict.keys() :
        filename=os.path.join(app.config['UPLOAD_FOLDER'], x)
        #catpath=os.path.join(app.config['CAT_FOLDER'],final_dict[x])
        shutil.move(filename,final_dict[x])
        catpath=os.path.join(catfolder,final_dict[x])
    zf.write(catpath)
    zf.close()