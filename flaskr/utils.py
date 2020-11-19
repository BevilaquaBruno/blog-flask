IMGS_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename, t):
  if t == 'img':
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMGS_EXTENSIONS
  return False