from flask import Flask,render_template,Response,send_file,redirect,url_for,render_template,request
from download3 import *

app = Flask(__name__)

app.config['SECRET'] = 'secret!'

         

#default Index.html page shows.
@app.route('/')
def index():
    return render_template('./index.html', status = "Please Provide Your URl..")




@app.route('/scrap_image', methods = ['POST'])
def download_image():
    url = request.form['url']
    print(url)
    try:
        crop = request.form['crop']
    except:
        crop = 'off'
    
    print(crop)
    try:
        upscale = request.form['upscale']
    except:
        upscale = 'off'
    
    print(upscale)
    if url.startswith('https://detail.1688.com/offer/'):

        if crop == 'on':
            print("Crop is on")
            crop = True
        else:
            crop = False
        if upscale == 'on':
            upscale = True
        else:
            upscale = False
        zip_path, file_name = load_the_url(url, crop,upscale)
        return redirect(url_for('download_on_your_device',file = file_name))


    else:
        return render_template('index.html', status = 'Wrong Url ....')



@app.route('/download_image/<file>', methods = ['get'])
def download_on_your_device(file):
    return send_file(f'static/{file}.zip', as_attachment=True)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
