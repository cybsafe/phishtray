import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import format from 'date-fns/format';
import Markdown from 'react-remarkable';

import EmailCard from './EmailCard';

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
        <EmailCard
          name={email.from.name}
          photoUrl={email.from.photoUrl}
          role={email.from.role}
          email={email.from.email}
          triggerText={
            <img
              className={css({ width: 60, height: 60, borderRadius: '50%' })}
              src={email.from.photoUrl}
              alt=""
            />
          }
          direction="right"
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
          className={css({
            color: '#B8B8B8',
            fontSize: 18,
            display: 'flex',
            flexDirection: 'row',
          })}
        >
          <p>From: </p>
          <EmailCard
            name={email.from.name}
            photoUrl={email.from.photoUrl}
            role={email.from.role}
            email={email.from.email}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {email.from.name ? email.from.name + ' ' : ' '}
                {String.fromCharCode(8744)}
              </a>
            }
          />
        </div>
        <div
          className={css({
            color: '#B8B8B8',
            fontSize: 18,
            display: 'flex',
            flexDirection: 'row',
          })}
        >
          <p>To: </p>
          <EmailCard
            name={'You'}
            photoUrl={'https://randomuser.me/api/portraits/women/83.jpg'}
            email={'you@yourcompany.com'}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {'You '}
                {String.fromCharCode(8744)}
              </a>
            }
          />
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
