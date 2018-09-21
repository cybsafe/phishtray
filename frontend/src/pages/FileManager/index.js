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
  loadFiles,
  removeFile,
  displayFile,
  hideFile,
  hideAndDeleteFile,
} from '../../reducers/fileManagerReducer';

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
    await this.props.loadFiles();
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
            {files.map(file => (
              <FileListItem
                key={file.id}
                file={file}
                deleteFileHandler={this.deleteFileHandler}
                displayFileModalHandler={this.displayFileModalHandler}
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
  }),
  {
    loadFiles,
    removeFile,
    displayFile,
    hideFile,
    hideAndDeleteFile,
  }
)(FileManager);
