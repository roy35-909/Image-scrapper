from flask import Flask,render_template,Response
# from download3 import load_the_url

app = Flask(__name__)

app.config['SECRET'] = 'secret!'

         

#default Index.html page shows.
@app.route('/')
def index():
    return render_template('./index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
