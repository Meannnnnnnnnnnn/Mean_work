from flask import Flask, jsonify, render_template
import json

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('pos_server.html')

@app.route('/position')
def get_position():
    try:
        with open('/tmp/latest_position.json', 'r') as infile:
            position_data = json.load(infile)
        return jsonify(position_data)
    except FileNotFoundError:
        return jsonify({"error": "No position data available"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
