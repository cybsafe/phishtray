import React, { useEffect } from 'react';
import styled, { css } from 'react-emotion';
import { useSelector, useDispatch } from 'react-redux';
import { InlineLoading } from 'carbon-components-react';
import FileListItem from './components/FileListItem';
import FileModal from './components/FileModal';
import {
  getFiles,
  getLastRefreshed,
  getModal,
} from '../../selectors/fileManagerSelectors';
import {
  loadFiles,
  removeFile,
  displayFile,
  hideFile,
  hideAndDeleteFile,
} from '../../actions/fileManagerActions';
import { logAction } from '../../utils';
import actionTypes from '../../config/actionTypes';
import withErrorBoundary from '../../errors/ErrorBoundary';

const columns = [
  {
    width: '30',
    header: '',
  },
  {
    width: '30',
    header: 'Description',
  },
  {
    width: '20',
    header: 'Date created',
  },
  {
    width: '20',
    header: '',
  },
];

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  margin: '0 50px',
  paddingBottom: 80,
});

const Table = styled('table')({
  width: '100%',
});

const TableHead = () => (
  <thead>
    <tr>
      {columns.map((column, index) => {
        const width = `${column.width}%`;
        return (
          <th
            key={index}
            className={css({
              width,
              padding: '50px 0 10px',
              textAlign: 'left',
              color: '#5596e6',
            })}
          >
            {column.header}
          </th>
        );
      })}
    </tr>
  </thead>
);

const Loading = () => (
  <Container>
    <InlineLoading
      className={css({
        color: '#fff',
        justifyContent: 'center',
        marginTop: '20%',
        '& svg': { stroke: '#fff !important' },
      })}
      description="Loading"
    />
  </Container>
);

const FileManager = ({ location }) => {
  const files = useSelector(state => getFiles(state));
  const isLoaded = useSelector(state => getLastRefreshed(state) !== null);
  const modal = useSelector(state => getModal(state));
  const startTime = useSelector(state => state.exercise.startTime);
  const fileDeleted = useSelector(state => state.fileManager.fileDeleted);
  const participantId = useSelector(state => state.exercise.participant);
  const dispatch = useDispatch();

  const displayFileModalHandler = React.useCallback(
    fileUrl => {
      dispatch(displayFile(fileUrl));
    },
    [dispatch]
  );
  const deleteFileHandler = fileToDelete => {
    if (modal.isOpen && modal.fileUrl === fileToDelete.fileUrl) {
      dispatch(hideAndDeleteFile(fileToDelete.id));
    } else {
      dispatch(removeFile(fileToDelete.id));
    }
  };

  const hideFileModalHandler = () => {
    dispatch(hideFile());
  };

  const logActionsHandler = params => {
    return logAction({
      participantId: participantId,
      timeDelta: Date.now() - startTime,
      timestamp: new Date(),
      ...params,
    });
  };

  useEffect(() => {
    //view files when attributes passed from Email link
    const openModalFromAttachment = params => {
      if (params && params.attachment) {
        params.attachment.fileUrl &&
          displayFileModalHandler(params.attachment.fileUrl);
      }
    };

    //only load files once there are no files or a file have not been deleted
    async function dispatchLoadFiles() {
      files.length <= 0 && !fileDeleted && (await dispatch(loadFiles()));
    }

    openModalFromAttachment(location.params);
    dispatchLoadFiles();
    // eslint-disable-next-line
  }, [dispatch, displayFileModalHandler, fileDeleted, location.params]);

  if (!isLoaded) return <Loading />;
  return (
    <Container>
      {modal.isOpen && (
        <FileModal
          fileUrl={modal.fileUrl}
          isOpen={modal.isOpen}
          hideFileModalHandler={hideFileModalHandler}
        />
      )}
      <Table>
        <TableHead />
        <tbody>
          {files &&
            files.map(file => (
              <FileListItem
                key={file.id}
                file={file}
                deleteFileHandler={file => {
                  logActionsHandler({
                    actionType: actionTypes.fileDelete,
                    fileId: file.id,
                    fileName: file.fileName,
                  });
                  deleteFileHandler(file);
                }}
                displayFileModalHandler={file => {
                  logActionsHandler({
                    actionType: actionTypes.fileOpen,
                    fileId: file.id,
                    fileName: file.fileName,
                  });
                  displayFileModalHandler(file);
                }}
              />
            ))}
        </tbody>
      </Table>
    </Container>
  );
};

export default withErrorBoundary(FileManager);
