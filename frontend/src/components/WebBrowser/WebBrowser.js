import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import { MemoryRouter } from 'react-router-dom';

import { getWebpage } from '../../selectors/uiSelectors';
import { closeWebpage } from '../../actions/uiActions';

import { logAction } from '../../utils';
import actionTypes from '../../config/actionTypes';

const BrowserChrome = styled('div')({
  position: 'absolute',
  top: 30,
  left: 50,
  width: '95%',
  minHeight: '90%',
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

function UnLocked() {
  return (
    <svg width="12" height="16">
      <path d="M2.5 7V3.5a3.5 3.5 0 0 1 7 0V4h-1v-.5a2.5 2.5 0 0 0-5 0V7h7A1.5 1.5 0 0 1 12 8.5v6a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 0 14.5v-6A1.5 1.5 0 0 1 1.5 7h1zm-1 1a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-6a.5.5 0 0 0-.5-.5h-9z" />
    </svg>
  );
}

function Locked() {
  return (
    <svg
      width="16"
      height="16"
      className={css({
        fill: 'green',
        stroke: 'green',
      })}
    >
      <path d="M4.5 7V3.5a3.5 3.5 0 0 1 7 0V7h1A1.5 1.5 0 0 1 14 8.5v6a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 14.5v-6A1.5 1.5 0 0 1 3.5 7h1zm1 0h5V3.5a2.5 2.5 0 0 0-5 0V7zm-2 1a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-6a.5.5 0 0 0-.5-.5h-9z" />
    </svg>
  );
}

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
          flex: '0 0 1',
          width: 70,
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          marginRight: 10,
        })}
      >
        <BrowserHeaderButton
          onClick={() => onClose()}
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
        <span>
          {isSecure ? (
            <span className={css({ color: 'green' })}>
              <Locked /> Secure |
            </span>
          ) : (
            <UnLocked />
          )}{' '}
        </span>
        <span className={css({ color: isSecure ? 'green' : 'red' })}>
          {isSecure ? 'https' : 'http'}
        </span>
        <span>
          ://
          {url}
        </span>
      </div>
    </div>
  );
}

export class WebBrowser extends Component {
  logBrowserActions = params => {
    return logAction({
      participantId: this.props.participantId,
      timeDelta: Date.now() - this.props.startTime,
      timestamp: new Date(),
      website: this.props.webpage.link,
      websiteURL: this.props.webpage.url,
      isSecure: this.props.webpage.isSecure,
      emailId: this.props.emailId,
      ...params,
    });
  };

  render() {
    const {
      closeWebpage,
      webpage,
      enableClose,
      threads,
      activeThread,
    } = this.props;

    let threadProperties = {};

    if (activeThread && activeThread !== '') {
      const active = threads.filter(thread => thread.id === activeThread);
      threadProperties = active[0].threadProperties;
    }

    if (!webpage) {
      return null;
    }

    const ContentComponent = webpage.component;

    return (
      <BrowserChrome>
        <BrowserHeader
          onClose={() => {
            this.logBrowserActions({
              actionType: actionTypes.browserClose,
            });
            enableClose.page !== 'blockedPage' && closeWebpage();
          }}
          isSecure={webpage.isSecure}
          url={
            threadProperties.webPage
              ? threadProperties.webPage.url
              : webpage.url
          }
        />
        <MemoryRouter>
          <ContentComponent
            logBrowserActions={this.logBrowserActions}
            actionTypes={actionTypes}
          />
        </MemoryRouter>
      </BrowserChrome>
    );
  }
}

export default connect(
  state => ({
    emailId: state.ui.webBrowser ? state.ui.webBrowser.emailId : '',
    webpage: getWebpage(state),
    enableClose: state.ui.webBrowser,
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
    activeThread: state.exercise.activeThread,
    threads: state.exercise.threads,
  }),
  { closeWebpage }
)(WebBrowser);
