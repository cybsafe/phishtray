// @flow
import React, { Fragment } from 'react';
import { connect } from 'react-redux';
import styled, { css } from 'react-emotion';
import { Link } from 'react-router-dom';
import Markdown from 'react-markdown';
import moment from 'moment';

import EmailCard from './EmailCard';
import QuickReply from './QuickReply';

import { logAction, selectWebpageType } from '../../../utils';
import actionTypes from '../../../config/actionTypes';
import { loadFiles } from '../../../actions/fileManagerActions';

import { showWebpage } from '../../../actions/uiActions';

type Props = {
  email: Object,
  onReplyParams: Object,
  threadId: string,
  repliesRef: Object,
  activeThread: string,
  threads: Array<Object>,
  addFile: () => void,
  loadFiles: () => void,
  markThreadAsDeleted: () => void,
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

const FromAccountInitials = styled('div')({
  width: 60,
  height: 60,
  borderRadius: '50%',
  backgroundColor: '#1B87EC',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  color: 'white',
  fontSize: '2rem',
});

const FromAccountPhoto = styled('img')({
  width: 60,
  height: 60,
  borderRadius: '50%',
});

function EmailAttachments({ props }) {
  const {
    email,
    onReplyParams,
    addFile,
    loadFiles,
    threads,
    activeThread,
  } = props;
  const active = threads.filter(thread => thread.id === activeThread);

  const {
    interceptExercise,
    releaseCodes,
    webPage,
  } = active[0].threadProperties;

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
        })}
      >
        {email.attachments &&
          email.attachments.map(attachment => {
            if (webPage) {
              return (
                <a
                  className={css({
                    marginRight: 20,
                    textDecoration: 'none',
                    color: '#B8B8B8',
                    letterSpacing: '1.1px',
                    cursor: 'pointer',
                  })}
                  onClick={() => {
                    webPage &&
                      selectWebpageType(
                        interceptExercise,
                        releaseCodes,
                        props.showWebpage,
                        actionTypes.emailAttachmentDownload
                      );
                  }}
                >
                  {attachment.filename || attachment.fileName}
                </a>
              );
            } else {
              return (
                <Link
                  key={attachment.id}
                  to={{
                    pathname: '/files',
                    params: {
                      attachment,
                    },
                  }}
                  onClick={async () => {
                    await loadFiles();
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
              );
            }
          })}
      </div>
    </div>
  );
}

function EmailInfo({ email, threads, activeThread }) {
  const activeEmailThread = threads.filter(
    thread => thread.id === activeThread
  );
  const dateReceived = activeEmailThread[0].threadProperties.dateReceived;
  const date = dateReceived
    ? moment(dateReceived).format('dddd D MMM YYYY')
    : moment().format('dddd D MMM YYYY');

  const { fromAccount, toAccount } = email;
  const fromAccountSenderNames = fromAccount.name.split(' ');

  const onlyInitials =
    fromAccountSenderNames.length === 1
      ? fromAccountSenderNames[0].charAt(0)
      : fromAccountSenderNames[0].charAt(0) +
        fromAccountSenderNames[fromAccountSenderNames.length - 1].charAt(0);

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
          name={fromAccount.name}
          photoUrl={fromAccount.photoUrl}
          onlyInitials={onlyInitials}
          role={fromAccount.role}
          email={fromAccount.email}
          triggerText={
            fromAccount.photoUrl ? (
              <FromAccountPhoto src={fromAccount.photoUrl} alt="" />
            ) : (
              <FromAccountInitials>{onlyInitials}</FromAccountInitials>
            )
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
            name={fromAccount.name}
            photoUrl={fromAccount.photoUrl}
            role={fromAccount.role}
            email={fromAccount.email}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {fromAccount.name ? fromAccount.name + ' ' : ' '}
                {String.fromCharCode(8744)}
              </a>
            }
          />
        </EmailField>
        <EmailField>
          <p>To: </p>
          <EmailCard
            name={toAccount.name}
            photoUrl={toAccount.photoUrl}
            email={toAccount.email}
            role={toAccount.role}
            triggerText={
              <a
                className={css({
                  textDecoration: 'underline',
                  display: 'inline-block',
                })}
              >
                {toAccount.name ? toAccount.name + ' ' : ' '}
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
        {date}
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

function ReturnReplies({ props, items }) {
  const { showWebpage } = props;
  const {
    interceptExercise,
    releaseCodes,
    webPage,
  } = items[0].threadProperties;

  return !props.email.isReplied ? (
    <Fragment>
      <h3 ref={props.repliesRef}>
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
        onClick={() => {
          webPage &&
            selectWebpageType(interceptExercise, releaseCodes, showWebpage);
        }}
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

const Email = (props: Props) => {
  const active = props.threads.filter(
    thread => thread.id === props.activeThread
  );

  const { email, threads, activeThread } = props;
  return (
    <div
      className={css({
        maxWidth: 880,
        margin: '0 auto',
        padding: '0 40px',
      })}
    >
      <EmailInfo email={email} threads={threads} activeThread={activeThread} />

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
          <ReturnReplies items={active} props={props} />
        </Fragment>
      )}
    </div>
  );
};

export default connect(
  state => ({
    activeThread: state.exercise.activeThread,
    threads: state.exercise.threads,
    exercise: state.exercise,
  }),
  { showWebpage, loadFiles }
)(Email);
