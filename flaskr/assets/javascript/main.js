function init_filepond(field_id, file_list_id) {
  FilePond.registerPlugin(FilePondPluginImagePreview);
  FilePond.setOptions({
    server: 'uploads/work'
  });
  /*
  {
    url: ( (window.location.host == 'localhost:5000')?'http://':'https://' )+window.location.host,
    process: '/uploads/process',
    revert: '/uploads/revert',
    restore: '/uploads/restore/',
    load: '/uploads/load/',
    fetch: '/uploads/fetch/'
  }
   */
  const el = document.getElementById(field_id);
  const pond = FilePond.create( el );
  let fl = document.getElementById(file_list_id).innerText;
  file_list = remove_empty_spaces_array(fl.split(';'));
  for (let i = 0; i < file_list.length; i++) {
    const el = file_list[i];
    let pre = (window.location.host == 'localhost:5000')?'http://':'https://';
    pond.addFile(pre+window.location.host+'/uploads/'+el);
  }
  return pond;
}

function remove_empty_spaces_array(arr) {
  for (let i = 0; i < arr.length; i++) {
    arr[i] = arr[i].trim();
    if (arr[i] === '') {
      arr.splice(i,1);
    }
  }
  return arr;
}
