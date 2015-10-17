from flask import Flask, render_template
import webbrowser

app = Flask(__name__)      

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/tweetsfeed')
def hey():
  Rurl = "http://www.mashable.com"
  webbrowser.open(Rurl)
  # return render_template('index.html')

# if __name__ == "__main__":
#   app.run(debug=True)
#not sure if we need this anymore...
#@app.route('/<path:path>')
#def seeStaticFile(path):
#	return app.send_static_file(path);


