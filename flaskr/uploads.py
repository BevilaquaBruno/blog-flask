from flask import (
  Blueprint, send_from_directory, request, make_response
)
from werkzeug.utils import secure_filename
from flaskr.utils import (allowed_file)
from flaskr.myConfig import (
  BLANK_FILE, JAVASCRIPT_FOLDER, UPLOAD_FOLDER, UPLOAD_TEMP_FOLDER
)

import os
import uuid
import json

bp = Blueprint('uploads', __name__)


@bp.route('/uploads/img/', defaults={'filename': None})
@bp.route('/uploads/img/<filename>')
def uploaded_file(filename):
  if filename is None:
    filename = 'blank.jpg'
  file_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], filename)
  file_main = "%s%s" % (UPLOAD_FOLDER[:-1], filename)
  if os.path.isfile(file_temp):
    return send_from_directory(UPLOAD_TEMP_FOLDER[:-1], filename)
  elif os.path.isfile(file_main):
    return send_from_directory(UPLOAD_FOLDER[:-1], filename)
  else:
    return send_from_directory(UPLOAD_FOLDER[:-1], 'blank.jpg')

@bp.route('/uploads/javascript/<jsfile>')
def uploaded_javascript(jsfile):
  return send_from_directory(JAVASCRIPT_FOLDER[:-1], jsfile)

@bp.route('/uploads/work/', methods=('POST', 'DELETE', 'GET'))
def work():
  if request.method == 'POST':
    if 'photo' in request.files:
      photo = request.files['photo']
      if photo is not None and photo.filename != '':
        if allowed_file(photo.filename, 'img'):
          unique_filename = "%s.%s" % (str(uuid.uuid4()).replace('-', '_'), photo.filename.rsplit('.', 1)[1].lower() )
          photoname = secure_filename(unique_filename)
          photo.save(os.path.join(UPLOAD_TEMP_FOLDER, photoname))
          return photoname
        else:
          photoname = ''
      else:
        photoname = ''
    else:
      photoname = ''
  elif request.method == 'DELETE':
    file = json.loads(request.data.decode('utf-8'))['photo']
    if file == 'blank.jpg':
      return 'Are you kidding me?'
    file_path = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], file)
    if(not os.path.exists(file_path)):
      file_path = "%s%s" % (UPLOAD_FOLDER[:-1], file)
    os.remove(file_path)
    return 'deleted'
  elif request.method == 'GET':
    load = request.args.get('load')
    file_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], load)
    if os.path.isfile(file_temp):
      response = make_response(send_from_directory(UPLOAD_TEMP_FOLDER[:-1], load))
    else:
      response = make_response(send_from_directory(UPLOAD_FOLDER[:-1], load))

    response.headers['Content-Disposition'] = 'inline'
    response.headers['filename'] = load
    return response