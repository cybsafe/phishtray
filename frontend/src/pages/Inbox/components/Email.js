import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import format from 'date-fns/format';
import Markdown from 'react-remarkable';

import QuickReply from './QuickReply';

type Props = {
  email: Object,
};

const ActionLink = styled('a')({
  marginRight: 20,
  textDecoration: 'none',
  color: '#B8B8B8',
  fontWeight: 'bold',
  letterSpacing: '1.1px',
});

const BodyContainer = styled('div')({
  marginTop: 40,
  color: '#666',
  '& p': {
    marginBottom: 20,
    fontSize: 20,
  },
});

function EmailActions() {
  return (
    <div
      className={css({
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-end',
        marginTop: '20px',
      })}
    >
      <ActionLink href="#">Reply</ActionLink>
      <ActionLink href="#">Forward</ActionLink>
      <ActionLink href="#">Delete</ActionLink>
      <ActionLink href="#">Report</ActionLink>
    </div>
  );
}

function EmailInfo({ email }) {
  return (
    <div
      className={css({
        display: 'flex',
        flexDirection: 'row',
        marginTop: 40,
      })}
    >
      <div className={css({ flex: 0, flexBasis: '60px' })}>
        <img
          className={css({ width: 60, height: 60, borderRadius: '50%' })}
          src={email.from.photoUrl}
        />
      </div>
      <div
        className={css({
          flex: 1,
          flexDirection: 'column',
          marginLeft: 20,
          display: 'flex',
          marginTop: 10,
        })}
      >
        <div
          className={css({ marginBottom: 10, color: '#B8B8B8', fontSize: 18 })}
        >
          From: <a href="#">{email.from.name}</a>
        </div>
        <div className={css({ color: '#B8B8B8', fontSize: 18 })}>
          To: <a href="#">You</a>
        </div>
      </div>
      <div
        className={css({
          flex: 1,
          textAlign: 'right',
          paddingTop: 10,
          color: '#B8B8B8',
          letterSpacing: '1px',
        })}
      >
        {format(email.timestamp, 'dddd D MMM YYYY')}
      </div>
    </div>
  );
}

export default class Email extends Component<Props> {
  render() {
    return (
      <div
        className={css({
          maxWidth: 880,
          margin: '0 auto',
          padding: '0 40px',
        })}
      >
        <EmailActions />
        <EmailInfo email={this.props.email} />

        <h3
          className={css({
            marginTop: 40,
            fontSize: 40,
            color: '#333',
            letterSpacing: '1.2px',
          })}
        >
          {this.props.email.subject}
        </h3>

        <Markdown source={this.props.email.body} container={BodyContainer} />
        {this.props.email.replies && (
          <QuickReply replies={this.props.email.replies} />
        )}
      </div>
    );
  }
}
