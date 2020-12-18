function init_filepond(field_id, file_list_id) {
  FilePond.registerPlugin(FilePondPluginImagePreview);
  let pre = (window.location.host == 'localhost:5000')?'http://':'https://';
  FilePond.setOptions({
    server: pre+window.location.host+'/uploads/work'
  });

  const el = document.getElementById(field_id);
  let fl = document.getElementById(file_list_id).innerText;
  file_list_div = remove_empty_spaces_array(fl.split(';'));
  let file_list = [];
  if (file_list_div.length > 0 && ';' != fl) {
    for (let i = 0; i < file_list_div.length; i++) {
      const file = file_list_div[i];
      file_list.push({ source: file, options: { type: "local" } });
    }
  }
  const pond = FilePond.create( el, {
    files: file_list,
    acceptedFileTypes: ['image/png', 'image/jpeg']
  });
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
