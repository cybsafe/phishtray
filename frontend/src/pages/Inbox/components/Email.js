// @flow
import React, { Fragment, createRef } from 'react';
import styled, { css } from 'react-emotion';
import { Link } from 'react-router-dom';
import format from 'date-fns/format';
import Markdown from 'react-markdown';

import EmailCard from './EmailCard';
import QuickReply from './QuickReply';

import { logAction } from '../../../utils';
import actionTypes from '../../../config/actionTypes';
import Button from '../../../components/Button/ReplyButton';

type Props = {
  email: Object,
  onReplyParams: Object,
  threadId: string,
  addFile: () => void,
  markThreadAsDeleted: () => void,
  addReplyToEmail: () => void,
};

const Divider = styled('p')({
  borderBottom: '1px solid #CCC',
  margin: '20px 0px 20px',
});

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

function EmailAttachments({ props }) {
  const { email, onReplyParams, addFile } = props;
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
        {email.attachments &&
          email.attachments.map(attachment => (
            <Link
              key={attachment.id}
              to={{
                pathname: '/files',
                params: {
                  attachment,
                },
              }}
              onClick={() => {
                logAction({
                  actionType: actionTypes.emailAttachmentDownload,
                  fileName: attachment.filename,
                  fileId: attachment.id,
                  participantId: onReplyParams.participantId,
                  timeDelta: Date.now() - onReplyParams.startTime,
                  emailId: onReplyParams.emailId,
                  timestamp: new Date(),
                });
                addFile(attachment);
              }}
              className={css({
                marginRight: 20,
                textDecoration: 'none',
                color: '#B8B8B8',
                letterSpacing: '1.1px',
              })}
            >
              > {attachment.filename || attachment.fileName}
            </Link>
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
            name={email.toAccount.name}
            photoUrl={email.toAccount.photoUrl}
            email={email.toAccount.email}
            role={email.toAccount.role}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {email.toAccount.name ? email.toAccount.name + ' ' : ' '}
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
      onClick={() => {
        const { onReplyParams, showWebpage } = props;
        logAction({
          actionType: actionTypes.emailLinkOpen,
          participantId: onReplyParams.participantId,
          timeDelta: Date.now() - onReplyParams.startTime,
          emailId: onReplyParams.emailId,
          link: props.href.substring(1),
          timestamp: new Date(),
        });
        showWebpage(props.href.substring(1), onReplyParams.emailId);
      }}
      href="#"
    >
      {props.children}
    </a>
  );
}

function ReturnReplies({ props }) {
  return !props.email.isReplied ? (
    <Fragment>
      <h3 ref={props.myRef}>
        You have {props.email.replies.length} option(s) to reply:
      </h3>
      <QuickReply
        logActionParams={props.onReplyParams}
        setSelectedReply={props.setSelectedReply}
        setSelectedReplyParams={{
          threadId: props.threadId,
          emailid: props.email.id,
        }}
        replies={props.email.replies}
      />
    </Fragment>
  ) : (
    <Fragment>
      <h3>You replied to this email:</h3>
      <Markdown
        source={props.email.replies[0].message}
        renderers={{
          paragraph: Paragraph,
          heading: Heading,
        }}
        className={css({ marginTop: '1em' })}
      />
    </Fragment>
  );
}

const Email = (props: Props) => (
  <div
    className={css({
      maxWidth: 880,
      margin: '0 auto',
      padding: '0 40px',
    })}
  >
    <EmailInfo email={props.email} />

    <h3
      className={css({
        marginTop: 40,
        fontSize: 40,
        color: '#333',
        letterSpacing: '1.2px',
      })}
    >
      {props.email.subject}
    </h3>

    <Markdown
      source={props.email.body}
      renderers={{
        link: linkProps => RouterLink({ ...linkProps, ...props }),
        paragraph: Paragraph,
        heading: Heading,
      }}
    />
    {props.email.attachments.length > 0 && <EmailAttachments props={props} />}
    {props.email.replies.length > 0 && (
      <Fragment>
        <Divider />
        <ReturnReplies props={props} />
      </Fragment>
    )}
  </div>
);

export default Email;
