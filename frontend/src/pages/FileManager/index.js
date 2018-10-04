import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
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
  minHeight: '100%',
  margin: 50,
  marginTop: 0,
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

export class FileManager extends Component {
  async componentDidMount() {
    //only load files once there are no files or a file have not been deleted
    this.props.files.length <= 0 &&
      !this.props.fileDeleted &&
      (await this.props.loadFiles());
    //view files when attributes passed from Email link
    if (this.props.location.params && this.props.location.params.attachment) {
      this.props.location.params.attachment.fileUrl &&
        this.displayFileModalHandler(
          this.props.location.params.attachment.fileUrl
        );
    }
  }

  deleteFileHandler = fileToDelete => {
    const { modal, removeFile, hideAndDeleteFile } = this.props;
    if (modal.isOpen && modal.fileUrl === fileToDelete.fileUrl) {
      hideAndDeleteFile(fileToDelete.id);
    } else {
      removeFile(fileToDelete.id);
    }
  };

  displayFileModalHandler = fileUrl => {
    this.props.displayFile(fileUrl);
  };

  hideFileModalHandler = () => {
    this.props.hideFile();
  };

  logActionsHandler = params => {
    return logAction({
      participantId: this.props.participantId,
      timeDelta: Date.now() - this.props.startTime,
      timestamp: new Date(),
      ...params,
    });
  };

  render() {
    const { files, isLoaded, modal } = this.props;
    if (!isLoaded) return <Loading />;
    return (
      <Container>
        {modal.isOpen && (
          <FileModal
            fileUrl={modal.fileUrl}
            hideFileModalHandler={this.hideFileModalHandler}
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
                    this.logActionsHandler({
                      actionType: 'file_delete',
                      fileId: file.id,
                      fileName: file.fileName,
                    }),
                      this.deleteFileHandler(file);
                  }}
                  displayFileModalHandler={file => {
                    this.logActionsHandler({
                      actionType: 'file_open',
                      fileId: file.id,
                      fileName: file.fileName,
                    }),
                      this.displayFileModalHandler(file);
                  }}
                />
              ))}
          </tbody>
        </Table>
      </Container>
    );
  }
}

export default connect(
  state => ({
    files: getFiles(state),
    isLoaded: getLastRefreshed(state) !== null,
    modal: getModal(state),
    startTime: state.exercise.startTime,
    fileDeleted: state.fileManager.fileDeleted,
    participantId: state.exercise.participant,
  }),
  {
    loadFiles,
    removeFile,
    displayFile,
    hideFile,
    hideAndDeleteFile,
  }
)(FileManager);
