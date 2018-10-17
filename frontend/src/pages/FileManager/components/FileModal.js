import React from 'react';
import styled from 'react-emotion';
import { Modal } from 'carbon-components-react';

const ModalContainer = styled('div')`
  & .bx--modal-footer {
    display: none;
  }
`;

const FileImage = styled('img')({
  maxHeight: '100%',
  maxWidth: '100%',
  paddingBottom: 5,
});

const FileModal = ({ fileUrl, isOpen, hideFileModalHandler }) => (
  <ModalContainer>
    <Modal open={isOpen} onRequestClose={hideFileModalHandler}>
      <FileImage src={fileUrl} />
    </Modal>
  </ModalContainer>
);

export default FileModal;
