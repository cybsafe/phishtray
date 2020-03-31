import React from 'react';
import styled, { css } from 'react-emotion';
import { useDispatch } from 'react-redux';
import { showWebpage } from '../../actions/uiActions';
import withErrorBoundary from '../../errors/ErrorBoundary';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  paddingTop: 100,
  position: 'relative',
});

const LinkContainer = styled('a')({
  display: 'block',
  cursor: 'pointer',
  marginRight: 50,
});

const WebsiteIcon = styled('div')({
  width: 200,
  height: 200,
  borderRadius: '12px',
});

const WebsiteTitle = styled('h3')({
  textAlign: 'center',
  marginTop: 25,
  color: '#333',
});

function Web() {
  const dispatch = useDispatch();

  const handleWebsiteClick = websiteId => {
    return event => {
      event.preventDefault();
      dispatch(showWebpage(websiteId));
    };
  };

  return (
    <Container>
      <LinkContainer onClick={handleWebsiteClick('mypayment')}>
        <WebsiteIcon className={css({ backgroundColor: '#e84118' })} />
        <WebsiteTitle>My Money Transfer</WebsiteTitle>
      </LinkContainer>
      <LinkContainer onClick={handleWebsiteClick('bluestar')}>
        <WebsiteIcon className={css({ backgroundColor: '#192a56' })} />
        <WebsiteTitle>Bluestar</WebsiteTitle>
      </LinkContainer>
    </Container>
  );
}

export default withErrorBoundary(Web);
