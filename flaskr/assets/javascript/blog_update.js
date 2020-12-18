window.onload = function(){
  let photo_pond = init_filepond('photo', 'file_list');
  document.querySelector('.filepond--root').addEventListener('FilePond:removefile', e => {
    console.log(e.detail.file.filename);
    axios({
      method: 'DELETE',
      url: '/uploads/work',
      data: {
        photo: e.detail.file.filename
      }
    }).then(function (response) {
      console.log(response.data);
    }).catch(function (error) {
      console.log(error);
    });
  });
}