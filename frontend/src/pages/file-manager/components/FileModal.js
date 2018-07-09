import React from 'react';
import styled, { css } from 'react-emotion';

const ImageContainer = styled('div')({
  position: 'absolute',
  top: '50%',
  left: '55%',
  transform: 'translate(-50%, -50%)',
  border: '1px solid #e6e6e6',
  background: '#ffffff',
  borderRadius: 4,
  padding: 10,
  zIndex: 99,
  maxHeight: 400,
  maxWidth: 500,
  textAlign: 'center',
});

const FileImage = styled('img')({
  maxHeight: '100%',
  maxWidth: '100%',
  paddingBottom: 5,
});

export default function FileModal({ fileUrl, hideFileModalHandler }) {
  return (
    <ImageContainer>
      <FileImage src={fileUrl} />
      <a
        className={css({
          fontSize: 16,
          fontWeight: 400,
          textDecoration: 'none',
          color: '#5596e6',
          cursor: 'pointer',
        })}
        onClick={hideFileModalHandler}
      >
        Close
      </a>
    </ImageContainer>
  );
}
