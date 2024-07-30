from flask import Flask, request, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template_string('''
        <!doctype html>
        <title>Upload File</title>
        <h1>Upload File</h1>
        <form action="" method="post" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>
    ''')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'File uploaded: {filename}'

if __name__ == '__main__':
    app.run(debug=True)
