from flask import Flask , send_file, send_from_directory, safe_join, abort ,render_template
from flask_ngrok import run_with_ngrok





UPLOAD_DIRECTORY  = 'C:\\Users\\USER\\Desktop\\discordBot'
app = Flask(__name__)
run_with_ngrok(app)

@app.route("/hi/<filename>" , methods=['POST' ,'GET'])
def hi(filename):

    safe_path = '1.mp3'

    try:
        return render_template('index.html' , message = filename)
    except FileNotFoundError:
        abort(404)

@app.route("/<filename>" , methods=['POST' ,'GET'])
def download(filename):
    
    try:
        return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

app.run()


if __name__ == "__main__":
    app.run()

