import { getAllFiles } from '../data/files';

export function loadFiles() {
  return async dispatch => {
    const files = getAllFiles();
    return dispatch({
      type: 'fileManager/LOAD_FILES',
      payload: files,
    });
  };
}

export function addFile(file) {
  return {
    type: 'fileManager/ADD_FILE',
    file
  };
}

export function removeFile(fileId) {
  return {
    type: 'fileManager/REMOVE_FILE',
    payload: {
      fileId,
    },
  };
}

export function displayFile(fileUrl) {
  return {
    type: 'fileManager/DISPLAY_FILE',
    payload: {
      fileUrl,
    },
  };
}

export function hideFile() {
  return {
    type: 'fileManager/HIDE_FILE',
  };
}

export function hideAndDeleteFile(fileId) {
  return {
    type: 'fileManager/HIDE_AND_DELETE_FILE',
    payload: {
      fileId,
    },
  };
}
