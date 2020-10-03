from flask import request, redirect, url_for, send_from_directory

from photo_frame import image_gallery
from photo_frame import upload_form

def init_app(app):
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
        if 'x-ios-shortcut' in request.headers:
          filename = image_gallery.save_from_data(request.data)
          return redirect(url_for('show_photo', filename=filename))
        else:
          if 'file' not in request.files:
              return redirect(request.url)

          file = request.files['file']

          if file.filename == '':
              return redirect(request.url)

          if file and image_gallery.allowed_file(file.filename):
              filename = image_gallery.save_photo(file)
              return redirect(url_for('show_photo', filename=filename))

    return upload_form.render()
