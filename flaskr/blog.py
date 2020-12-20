from flask import (
  Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.utils import (allowed_file, IMGS_EXTENSIONS)
from flaskr.myConfig import (UPLOAD_FOLDER, UPLOAD_TEMP_FOLDER)

import os
import shutil

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
  db = get_db()
  posts = db.execute(
    'SELECT p.id, p.title, p.body, p.created, p.author_id, p.photo, u.username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY p.created DESC'
  ).fetchall()
  data = dict(
    posts= posts,
    img_path= UPLOAD_FOLDER
  )
  return render_template('blog/index.html.jinja', data=data)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    photo = request.form['photo']
    error = None
    
    file_path_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], photo)
    if os.path.exists(file_path_temp) is False:
      error = 'Error in file, try to make upload again.'

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'INSERT INTO post (title, body, photo, author_id)'
        ' VALUES (?, ?, ?, ?)',
        (title, body, photo, g.user['id'])
      )
      db.commit()
      if photo is not None:
        if allowed_file(photo, 'img'):
          file_path = "%s%s" % (UPLOAD_FOLDER[:-1], photo)
          shutil.move(file_path_temp, file_path)
        else:
          exts = ', '.join(IMGS_EXTENSIONS)
          flash("Extensão não permitida, são permitidas: " + exts)
      return redirect(url_for('blog.index'))
  return render_template('blog/create.html.jinja')

def get_post(id, check_author=True):
  post = get_db().execute(
    'SELECT p.id, p.title, p.body, p.created, p.photo, p.author_id, u.username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
     (id,)
  ).fetchone()

  if post is None:
    abort(404, 'Post id {0} doesn\'t exist.'.format(id))

  if check_author and post['author_id'] != g.user['id']:
    abort(403)

  return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
  post = get_post(id)

  if request.method == 'POST':
    title = request.form['title']
    body = request.form['body']
    photoname = None
    if 'photo' in request.form:
      photoname = request.form['photo']
    error = None
    action_photo = None
    photo = None
    
    if post['photo'] != '' and photoname is None:
      action_photo = 'delete'
      photo = None
    elif post['photo'] != photoname:
      action_photo = 'overwrite'
      photo = photoname
      if not allowed_file(photo, 'img'):
        exts = ', '.join(IMGS_EXTENSIONS)
        flash("Extensão não permitida, são permitidas: " + exts)
    else:
      action_photo = 'maintain'
      photo = post['photo']

    if not title:
      error = 'Title is required.'

    if error is not None:
      flash(error)
    else:
      db = get_db()
      db.execute(
        'UPDATE POST set title = ?, body = ?, photo = ? WHERE id = ?',
        (title, body, photo, id)
      )
      db.commit()
      old_file_path = "%s%s" % (UPLOAD_FOLDER[:-1], post['photo'])
      if action_photo == 'delete':
        if(os.path.exists(old_file_path)):
          os.remove(old_file_path)
      elif action_photo == 'overwrite':
        if(os.path.exists(old_file_path)):
          os.remove(old_file_path)
        file_path_temp = "%s%s" % (UPLOAD_TEMP_FOLDER[:-1], photo)
        file_path = "%s%s" % (UPLOAD_FOLDER[:-1], photo)
        shutil.move(file_path_temp, file_path)
      return redirect(url_for('blog.index'))

  data = dict(post=post, img_path=UPLOAD_FOLDER)
  return render_template('blog/update.html.jinja', data=data)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
  post = get_post(id)
  db = get_db()
  db.execute('DELETE FROM post WHERE id = ?', (id,))
  db.commit()
  file_path = "%s%s" % (UPLOAD_FOLDER[:-1], post['photo'])
  if(os.path.exists(file_path)):
    os.remove(file_path)

  return redirect(url_for('blog.index'))
