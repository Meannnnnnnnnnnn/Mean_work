from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the root route
@app.route('/')
def index():
    return "Scenery is BEAUTIFUL"

# # Define an echo route that echoes back JSON data sent in a POST request
# @app.route('/echo', methods=['POST'])
# def echo():
#     data = request.json
#     return jsonify(data)

# Run the app
if __name__ == '__main__':
    app.run(host='172.20.10.6', port=8080)
