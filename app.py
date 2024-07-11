from flask import Flask, render_template, url_for, request
import sqlite3
import os
from image_test import *
from video_test import *
from audio_test import *

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('home.html')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/detectimage', methods=['GET', 'POST'])
def detectimage():
    if request.method == 'POST':

        src = "static/imgs/"+request.form['src']
        dst = "static/imgs/"+request.form['dst']
        out = "static/image_output/output.jpg"

        command = f"python main.py --src {src} --dst {dst} --out {out} --correct_color"
        os.system(command)

        return render_template('Image.html', inputimage=dst, outputimage=out)
    return render_template('Image.html')

@app.route('/detectvideo', methods=['GET', 'POST'])
def detectvideo():
    if request.method == 'POST':
        src = "static/imgs/"+request.form['src']
        dst = "static/videos/"+request.form['dst']
        out = "static/video_output/output.mp4"

        command = f"python main_video.py --src_img {src} --video_path {dst} --show --correct_color --save_path {out}"
        os.system(command)

        return render_template('Video.html', inputvideo=dst, outputvideo=out)
    return render_template('Video.html')

@app.route('/detectlive', methods=['GET', 'POST'])
def detectlive():
    if request.method == 'POST':
        src = "static/imgs/"+request.form['src']
        out = "static/video_output/output.mp4"

        command = f"python main_video.py --src_img {src} --show --correct_color --save_path {out}"
        os.system(command)
        return render_template('Live.html', inputvideo='static/videos/input.mp4', outputvideo=out)
    return render_template('Live.html')

@app.route('/detection')
def detection():
    return render_template('testimage.html')


@app.route('/testimage', methods=['GET', 'POST'])
def testimage():
    if request.method == 'POST':

        src = "static/imgs/"+request.form['src']
        out = "static/testimage_output/output.jpg"

        process_image(src, out)

        return render_template('testimage.html', inputimage=src, outputimage=out)
    return render_template('testimage.html')

@app.route('/testvideo', methods=['GET', 'POST'])
def testvideo():
    if request.method == 'POST':
        src = "static/videos/"+request.form['src']
        out = "static/testvideo_output/output.mp4"

        process_video(src, out)

        return render_template('testvideo.html', inputvideo=src, outputvideo=out)
    return render_template('testvideo.html')

@app.route('/testaudio', methods=['GET', 'POST'])
def testaudio():
    if request.method == 'POST':
        src = "static/audio/"+request.form['src']
        out = runtest(src)
        return render_template('testaudio.html', inputaudio=src, output=out)
    return render_template('testaudio.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
