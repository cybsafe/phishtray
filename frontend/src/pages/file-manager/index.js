import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { remove } from 'lodash';

import { getAllFiles } from '../../data/files';

import FileListItem from './components/FileListItem';

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

function TableHead() {
  return (
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
}

export default class FileManager extends Component {
  constructor() {
    super();
    this.state = { files: getAllFiles() };
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleDelete(fileId) {
    const files = this.state.files;
    const updatedFiles = remove(files, file => file.id !== fileId);
    this.setState({ files: updatedFiles });
  }

  render() {
    return (
      <Container>
        <Table>
          <TableHead />
          <tbody>
            {this.state.files.map((file, index) => {
              const isOdd = (index + 1) % 2;
              return <FileListItem key={file.id} file={file} isOdd={isOdd} files={this.state.files} handleDelete={this.handleDelete}/>;
            })}
          </tbody>
        </Table>
      </Container>
    );
  }
}
