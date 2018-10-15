// @flow

type File = {
  id: string,
  fileName: string,
  description: string,
  dateCreated: string,
  fileUrl: string,
};

type State = {
  lastRefreshed: ?Date,
  files: File[],
  fileDeleted: boolean,
  modal: {
    isOpen: boolean,
    fileUrl: string,
  },
};

const INITIAL_STATE: State = {
  lastRefreshed: null,
  files: [],
  fileDeleted: false,
  modal: {
    isOpen: false,
    fileUrl: '',
  },
};

export default function reducer(
  state: State = INITIAL_STATE,
  action: Object = {}
) {
  switch (action.type) {
    case 'fileManager/LOAD_FILES': {
      return {
        ...state,
        lastRefreshed: new Date(),
        files: action.payload,
      };
    }
    case 'fileManager/ADD_FILE': {
      return {
        ...state,
        files: new Set([...state.files.map(item => item.id)]).has(
          action.file.id
        )
          ? [...state.files]
          : [...state.files, action.file],
      };
    }
    case 'fileManager/REMOVE_FILE': {
      return {
        ...state,
        files: state.files.filter(file => file.id !== action.payload.fileId),
        fileDeleted: true,
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
        fileDeleted: true,
      };
    }

    default: {
      return state;
    }
  }
}
