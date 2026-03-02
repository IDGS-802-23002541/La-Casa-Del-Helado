from flask import Flask, render_template
from flask import flash

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template("inicio.html")

if __name__ == '__main__':
	app.run(debug=True)