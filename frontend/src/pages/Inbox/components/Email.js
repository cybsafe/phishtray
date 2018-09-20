import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { Link } from 'react-router-dom';
import format from 'date-fns/format';
import Markdown from 'react-markdown';

import EmailCard from './EmailCard';
import QuickReply from './QuickReply';

import { logAction } from '../../../utils';

type Props = {
  email: Object,
};

const ActionLink = styled('button')({
  marginRight: 20,
  textDecoration: 'none',
  color: '#B8B8B8',
  fontWeight: 'bold',
  letterSpacing: '1.1px',
});

function ActionLinkwithClick({ data, title }) {
  return (
    <ActionLink
      onClick={() =>
        logAction({
          actionType: data.actionType,
          participantId: data.participantId,
          timeDelta: Date.now() - data.startTime,
          emailId: data.emailId,
          timestamp: new Date(),
        })
      }
    >
      {title}
    </ActionLink>
  );
}

function AttachmentLink({ attachment, onClickParams }) {
  return (
    <Link
      to="/files"
      onClick={() =>
        logAction({
          actionType: 'attachment_downloaded',
          participantId: onClickParams.participantId,
          timeDelta: Date.now() - onClickParams.startTime,
          emailId: onClickParams.emailId,
          timestamp: new Date(),
        })
      }
      className={css({
        marginRight: 20,
        textDecoration: 'none',
        color: '#B8B8B8',
        letterSpacing: '1.1px',
      })}
    >
      > {attachment.filename}
    </Link>
  );
}

const EmailField = styled('div')({
  color: '#B8B8B8',
  fontSize: 18,
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
});

const Heading = styled('h1')({
  marginTop: 40,
  color: '#666',
});

const Paragraph = styled('p')({
  color: '#666',
  marginBottom: 20,
  fontSize: 20,
});

function EmailActions({ onReplyParams }) {
  return (
    <div
      className={css({
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'flex-end',
        marginTop: '20px',
      })}
    >
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: 'emailReply',
        }}
        title="Reply"
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: 'emailForward',
        }}
        title="Forward"
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: 'emailDelete',
        }}
        title="Delete"
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: 'emailReport',
        }}
        title="Report"
      />
    </div>
  );
}

function EmailAttachments({ attachments, onClickParams }) {
  return (
    <div
      className={css({
        display: 'flex',
        flexDirection: 'column',
        marginTop: '50px',
      })}
    >
      <hr
        className={css({
          width: '100%',
          color: '#eee',
        })}
      />
      <h6>Attachments</h6>
      <div
        className={css({
          display: 'flex',
          flexDirection: 'row',
          marginTop: '20px',
          marginBottom: '20px',
        })}
      >
        {attachments &&
          attachments.map(attachment => (
            <AttachmentLink
              onClickParams={onClickParams}
              key={attachment.id}
              attachment={attachment}
            />
          ))}
      </div>
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
          name={email.fromAccount.name}
          photoUrl={email.fromAccount.photoUrl}
          role={email.fromAccount.role}
          email={email.fromAccount.email}
          triggerText={
            <img
              className={css({ width: 60, height: 60, borderRadius: '50%' })}
              src={email.fromAccount.photoUrl}
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
        <EmailField>
          <p>From: </p>
          <EmailCard
            name={email.fromAccount.name}
            photoUrl={email.fromAccount.photoUrl}
            role={email.fromAccount.role}
            email={email.fromAccount.email}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {email.fromAccount.name ? email.fromAccount.name + ' ' : ' '}
                {String.fromCharCode(8744)}
              </a>
            }
          />
        </EmailField>
        <EmailField>
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
        </EmailField>
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
        {format(Date.now(), 'dddd D MMM YYYY')}
      </div>
    </div>
  );
}

function RouterLink(props) {
  return (
    <a
      onClick={props.showWebpage(props.href.substring(1))}
      onMouseUp={() => {
        const { onReplyParams, showWebpage } = props;
        logAction({
          actionType: 'link_clicked',
          participantId: onReplyParams.participantId,
          timeDelta: Date.now() - onReplyParams.startTime,
          emailId: onReplyParams.emailId,
          link: props.href.substring(1),
          timestamp: new Date(),
        });
      }}
      href="#"
    >
      {props.children}
    </a>
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
        <EmailActions onReplyParams={this.props.onReplyParams} />
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

        <Markdown
          source={this.props.email.body}
          renderers={{
            link: props => RouterLink({ ...this.props, ...props }),
            paragraph: Paragraph,
            heading: Heading,
          }}
        />
        {this.props.email.attachments && (
          <EmailAttachments
            onClickParams={this.props.onReplyParams}
            attachments={this.props.email.attachments}
          />
        )}
        {this.props.email.replies && (
          <QuickReply
            onClickParams={this.props.onReplyParams}
            replies={this.props.email.replies}
          />
        )}
      </div>
    );
  }
}
