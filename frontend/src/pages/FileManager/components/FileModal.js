import React from 'react';
import styled from 'react-emotion';
import { Modal } from 'carbon-components-react';

const ModalContainer = styled('div')`
  & .bx--modal-footer {
    display: none;
  }
  .bx--modal-container {
    max-width: 80%;
  }
  .bx--modal-header {
    margin: 0;
  }
  .bx--modal-content {
    &::-webkit-scrollbar {
      -webkit-appearance: none;
      height: 11px;
    }
    &::-webkit-scrollbar-thumb {
      border-radius: 8px;
      border: 3px solid white;
      background-color: rgba(0, 0, 0, 0.5);
    }
  }
`;

const FileImage = styled('img')({
  maxHeight: 'inherit',
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
