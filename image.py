#program for viewing saved images from camera on your browser
from flask import Flask, render_template
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
@app.route('/index')
def show_index():
    #camera.read()
    full_filename="static/ims/color.jpg"
    return render_template("index.html", user_image = full_filename)
app.run(debug=1, host='0.0.0.0')

