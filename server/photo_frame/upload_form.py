def render():
  return '''
    <!doctype html>
    <title>Upload new Photo</title>
    <h1>Upload new Photo</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''