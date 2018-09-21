// @flow
import { getAllFiles } from '../data/files';
import { createSelector } from 'reselect';

type File = {
  id: string,
  fileName: string,
  description: string,
  dateCreated: string,
  fileUrl: string,
};

type State = {
  lastRefreshed: ?Date,
  files: [File],
  modal: {
    isOpen: boolean,
    fileUrl: ?string,
  },
};

const INITIAL_STATE = {
  lastRefreshed: null,
  files: [],
  modal: {
    isOpen: false,
  },
};

export default function reducer(state: State = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'fileManager/LOAD_FILES': {
      return {
        ...state,
        lastRefreshed: new Date(),
        files: action.payload,
      };
    }
    case 'fileManager/REMOVE_FILE': {
      return {
        ...state,
        files: state.files.filter(file => file.id !== action.payload.fileId),
      };
    }
    case 'fileManager/DISPLAY_FILE': {
      return {
        ...state,
        modal: {
          isOpen: true,
          fileUrl: action.payload.fileUrl,
        },
      };
    }
    case 'fileManager/HIDE_FILE': {
      return {
        ...state,
        modal: {
          isOpen: false,
        },
      };
    }
    case 'fileManager/HIDE_AND_DELETE_FILE': {
      return {
        ...state,
        modal: {
          isOpen: false,
        },
        files: state.files.filter(file => file.id !== action.payload.fileId),
      };
    }

    default: {
      return state;
    }
  }
}

// Actions
export function loadFiles() {
  return async dispatch => {
    const files = getAllFiles();
    return dispatch({
      type: 'fileManager/LOAD_FILES',
      payload: files,
    });
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

// Selectors
const filesSelector = state => state.fileManager;
export const getFiles = createSelector(
  filesSelector,
  fileManager => fileManager.files
);

export const getLastRefreshed = createSelector(
  filesSelector,
  fileManager => fileManager.lastRefreshed
);

export const getModal = createSelector(
  filesSelector,
  fileManager => fileManager.modal
);
