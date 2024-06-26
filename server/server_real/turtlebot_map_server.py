from flask import Flask, send_file, render_template

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('map_server.html')

@app.route('/map')
def map_image():
    return send_file('/home/rac/Mean_work/server/server_real/map.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
