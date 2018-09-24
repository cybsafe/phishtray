import thunk from 'redux-thunk';
import configureMockStore from 'redux-mock-store';
import reducer, {
  removeFile,
  displayFile,
  hideFile,
  hideAndDeleteFile,
  loadFiles,
  getFiles,
  getLastRefreshed,
  getModal,
} from '../../reducers/fileManagerReducer';
import { getAllFiles } from '../../data/files';

import { advanceTo, clear } from 'jest-date-mock';

const middleware = [thunk];
const mockStore = configureMockStore(middleware);

describe('fileManager', () => {
  describe('reducer', () => {
    beforeEach(() => {
      advanceTo();
    });

    afterEach(() => {
      clear();
    });

    it('should return the initial state', () => {
      const state = reducer();
      expect(state).toMatchObject({
        lastRefreshed: null,
        files: [],
        modal: {
          isOpen: false,
        },
      });
    });

    it('should handle LOAD_FILES', () => {
      const state = reducer([], {
        type: 'fileManager/LOAD_FILES',
        payload: getAllFiles(),
      });
      expect(state).toMatchObject({
        lastRefreshed: new Date(),
        files: getAllFiles(),
      });
    });

    it('should handle REMOVE_FILE', () => {
      const state = reducer(
        { files: getAllFiles() },
        {
          type: 'fileManager/REMOVE_FILE',
          payload: {
            fileId: '001',
          },
        }
      );
      expect(state).toMatchObject({
        files: getAllFiles().filter(file => file.id !== '001'),
      });
    });

    it('should handle DISPLAY_FILE', () => {
      const state = reducer([], {
        type: 'fileManager/DISPLAY_FILE',
        payload: {
          fileUrl: 'http://www.fileUrl.com',
        },
      });
      expect(state).toMatchObject({
        modal: {
          isOpen: true,
          fileUrl: 'http://www.fileUrl.com',
        },
      });
    });

    it('should handle HIDE_FILE', () => {
      const state = reducer([], {
        type: 'fileManager/HIDE_FILE',
      });
      expect(state).toMatchObject({
        modal: {
          isOpen: false,
        },
      });
    });

    it('should handle HIDE_AND_DELETE_FILE', () => {
      const state = reducer(
        {
          files: getAllFiles(),
        },
        {
          type: 'fileManager/HIDE_AND_DELETE_FILE',
          payload: {
            fileId: '002',
          },
        }
      );
      expect(state).toMatchObject({
        modal: {
          isOpen: false,
        },
        files: getAllFiles().filter(file => file.id !== '002'),
      });
    });
  });

  describe('actions', () => {
    describe('removeFile', () => {
      it('should return REMOVE_FILE type with the file id', () => {
        const action = removeFile('123');
        expect(action).toMatchObject({
          type: 'fileManager/REMOVE_FILE',
          payload: {
            fileId: '123',
          },
        });
      });
    });

    describe('loadFiles', () => {
      it('should return DISPLAY_FILE type with the file url', () => {
        const action = displayFile('http://www.fileUrl.com');
        expect(action).toMatchObject({
          type: 'fileManager/DISPLAY_FILE',
          payload: {
            fileUrl: 'http://www.fileUrl.com',
          },
        });
      });
    });

    describe('hideFile', () => {
      it('should return HIDE_FILE type', () => {
        const action = hideFile();
        expect(action).toMatchObject({
          type: 'fileManager/HIDE_FILE',
        });
      });
    });

    describe('hideAndDeleteFile', () => {
      it('should return HIDE_AND_DELETE_FILE type and the file id', () => {
        const action = hideAndDeleteFile('123');
        expect(action).toMatchObject({
          type: 'fileManager/HIDE_AND_DELETE_FILE',
          payload: {
            fileId: '123',
          },
        });
      });
    });

    describe('loadFiles', () => {
      it('should return LOAD_FILES type and the list of files', async () => {
        const store = mockStore({});
        const action = await store.dispatch(loadFiles());
        expect(action).toMatchObject({
          type: 'fileManager/LOAD_FILES',
          payload: getAllFiles(),
        });
      });
    });
  });

  describe('selectors', () => {
    const date = new Date();
    let mockFilesSelector;

    beforeAll(() => {
      mockFilesSelector = {
        fileManager: {
          files: [],
          lastRefreshed: date,
          modal: {},
        },
      };
    });

    describe('getFiles', () => {
      it('should return an array', () => {
        const getFilesSelector = getFiles.resultFunc(
          mockFilesSelector.fileManager
        );
        expect(getFilesSelector).toEqual([]);
      });
    });

    describe('getLastRefreshed', () => {
      it('should return a date', () => {
        const getLastRefreshedSelector = getLastRefreshed.resultFunc(
          mockFilesSelector.fileManager
        );
        expect(getLastRefreshedSelector).toEqual(date);
      });
    });

    describe('getModal', () => {
      it('should return an object', () => {
        const getModalSelector = getModal.resultFunc(
          mockFilesSelector.fileManager
        );
        expect(getModalSelector).toEqual({});
      });
    });
  });
});
