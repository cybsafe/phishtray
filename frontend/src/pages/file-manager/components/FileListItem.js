import React from 'react';
import styled, { css } from 'react-emotion';
import { Checkbox } from 'carbon-components-react';

const Cell = styled('td')(
  {
    fontSize: 20,
    fontWeight: 600,
    color: '#8897a2',
  },
  props => ({
    padding: props.isOdd ? '26px 0 34px' : '0 0 8px',
    backgroundColor: props.isOdd ? '#ffffff' : '#f4f7fb',
  })
);

export default function FileListItem({ file, isOdd, files, handleDelete }) {
  const checkboxId = `checkbox-file-${file.id}`;
  return (
    <tr>
      <Cell isOdd={isOdd} className={css({ paddingLeft: 20 })}>
        <Checkbox
          defaultChecked={false}
          indeterminate={true}
          id={checkboxId}
          className={css({ fontSize: 20, fontWeight: 600 })}
          labelText={file.fileName}
        />
      </Cell>
      <Cell isOdd={isOdd}>{file.description}</Cell>
      <Cell isOdd={isOdd}>{file.dateCreated}</Cell>
      <Cell isOdd={isOdd}>
        <a
          onClick={() => handleDelete(file.id)}
          className={css({
            fontSize: 16,
            fontWeight: 400,
            textDecoration: 'none',
            color: '#5596e6',
            cursor: 'pointer',
          })}
        >
          Delete
        </a>
      </Cell>
    </tr>
  );
}
