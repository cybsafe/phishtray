import React, { Component } from 'react';
import styled, { css } from 'react-emotion';

import websites from '../websites';

const BrowserChrome = styled('div')({
  position: 'absolute',
  top: -30,
  left: 20,
  width: '95%',
  height: '90%',
  backgroundColor: '#fff',
  boxShadow: '10px 10px 65px 0px rgba(0,0,0,0.5)',
  borderRadius: '4px',
});

const BrowserHeaderButton = styled('div')({
  width: 14,
  height: 14,
  borderRadius: '50%',
  marginRight: 8,
  cursor: 'pointer',
});

function BrowserHeader({ onClose, url, isSecure }) {
  return (
    <div
      className={css({
        backgroundColor: '#e8e8e8',
        paddingTop: 10,
        paddingBottom: 10,
        paddingLeft: 20,
        paddingRight: 20,
        width: '100%',
        display: 'flex',
      })}
    >
      <div
        className={css({
          flex: 0,
          width: 70,
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          marginRight: 10,
        })}
      >
        <BrowserHeaderButton
          onClick={onClose}
          className={css({ backgroundColor: '#f44' })}
        />
        <BrowserHeaderButton className={css({ backgroundColor: '#fb5' })} />
        <BrowserHeaderButton className={css({ backgroundColor: '#9b3' })} />
      </div>
      <div
        className={css({
          backgroundColor: '#fff',
          padding: '10px',
          borderRadius: 4,
          flex: 1,
        })}
      >
        <span className={css({ color: isSecure ? 'green' : 'red' })}>
          {isSecure ? 'https' : 'http'}
        </span>
        <span>://{url}</span>
      </div>
    </div>
  );
}

export default class WebBrowser extends Component {
  render() {
    const { onClose, websiteId } = this.props;
    const website = websites[websiteId];

    if (!website) {
      return (
        <BrowserChrome>
          <p>Can't find website</p>
        </BrowserChrome>
      );
    }

    const ContentComponent = website.component;

    return (
      <BrowserChrome>
        <BrowserHeader
          onClose={onClose}
          isSecure={website.isSecure}
          url={website.url}
        />
        <ContentComponent />
      </BrowserChrome>
    );
  }
}
