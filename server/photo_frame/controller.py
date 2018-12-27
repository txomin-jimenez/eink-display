from flask import Flask, flash, request, redirect, url_for, send_from_directory

import image_gallery
import upload_form

app = Flask(__name__)

@app.route('/photo_frame')
def random_photo():
  random_filename = image_gallery.random_photo()
  return redirect(url_for('show_photo', filename=random_filename))

@app.route('/photo_frame/<filename>')
def show_photo(filename):
  return send_from_directory(image_gallery.GALLERY_FOLDER, filename)

@app.route('/photo_frame/upload', methods=['GET', 'POST'])
def upload_photo():
  if request.method == 'POST':
      if 'file' not in request.files:
          flash('No file part')
          return redirect(request.url)

      file = request.files['file']

      if file.filename == '':
          flash('No selected file')
          return redirect(request.url)

      if file and image_gallery.allowed_file(file.filename):
          filename = image_gallery.save_photo(file)
          return redirect(url_for('show_photo', filename=filename))

  return upload_form.render()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)