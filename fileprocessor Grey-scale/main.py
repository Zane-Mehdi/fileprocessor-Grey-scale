from flask import Flask, render_template ,redirect,request, send_file,url_for
from werkzeug.utils import secure_filename
import os
from processor import processor
from flask_apscheduler import APScheduler


app = Flask(__name__)
UPLOAD_FOLDER= './static/process/'

ALLOWED_EXTENSIONS={'png','jpg','jpeg'}
##############
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
scheduler= APScheduler()
@app.route('/')
def home():
    return render_template('home.html', message='GREYSCALER')


@app.route('/process/',methods=['POST','GET'])
def process():
    f=request.files['file']
    if f.filename=='':
        return render_template('home.html', message='CHOOSE FILE')

    if f.filename.split('.')[1] in app.config['ALLOWED_EXTENSIONS']:
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
        processor(f.filename)
        return redirect(url_for('download',filename=f.filename))
    else:
        return render_template('home.html', message='Not A IMG')
    

@app.route('/download/<filename>')
def download(filename):
    filelocation = './static/process/'+filename
    return send_file(filelocation,as_attachment=True)


def emptyfolder():
    filelist=[f for f in os.listdir('./static/process/')]
    for f in filelist:
        os.remove(os.path.join('./static/process/',f))
    print('files cleared')
if __name__ == "__main__":
    scheduler.add_job(id='empty folder', func=emptyfolder,trigger='interval',seconds=1800)
    scheduler.start()
    app.run(debug=True)
