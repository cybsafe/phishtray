import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';

import { showWebpage } from '../../reducers/ui';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
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

class Web extends Component {
  handleWebsiteClick = websiteId => {
    return event => {
      event.preventDefault();
      this.props.showWebpage(websiteId);
    };
  };

  render() {
    return (
      <Container>
        <LinkContainer onClick={this.handleWebsiteClick('myoffice')}>
          <WebsiteIcon className={css({ backgroundColor: '#e84118' })} />
          <WebsiteTitle>My Office</WebsiteTitle>
        </LinkContainer>
        <LinkContainer onClick={this.handleWebsiteClick('fileshare')}>
          <WebsiteIcon className={css({ backgroundColor: '#192a56' })} />
          <WebsiteTitle>Fileshare</WebsiteTitle>
        </LinkContainer>
        <LinkContainer onClick={this.handleWebsiteClick('bank')}>
          <WebsiteIcon className={css({ backgroundColor: '#e84118' })} />
          <WebsiteTitle>Bank</WebsiteTitle>
        </LinkContainer>
      </Container>
    );
  }
}

export default connect(
  null,
  { showWebpage }
)(Web);
