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
  modal: {
    isOpen: boolean,
    fileUrl: string,
  },
};

const INITIAL_STATE: State = {
  lastRefreshed: null,
  files: [],
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
