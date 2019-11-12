// @flow
import React, { Fragment, useState } from 'react';
import { connect } from 'react-redux';
import styled, { css } from 'react-emotion';
import { Link } from 'react-router-dom';
import Markdown from 'react-markdown';
import moment from 'moment';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';

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

const EmailFieldInnerContainer = styled('div')`
  svg {
    transition: transform 0.4s ease-in-out;
  }
`;

const NameLink = styled('a')`
  &&& {
    cursor: pointer;
    text-decoration: underline;
    display: inline-block;
  }
  ${({ isHover }) =>
    isHover
      ? `
   svg {
      transition: transform 0.4s ease-in-out;
      transform: scale(-1, -1);
    }
  `
      : ''}
`;

const CustomLink = styled('button')`
  margin-right: 20px;
  letterspacing: 1.1px;
  cursor: pointer;
  background-color: transparent;
  border: none;
  font-size: ${({ attachment }) => (attachment ? '1rem' : '1.2rem')};
  text-decoration: ${({ attachment }) => (attachment ? 'none' : 'underline')};
  color: ${({ attachment }) => (attachment ? '#b8b8b8' : '#3d70b2')};
`;

const Icon = styled(FontAwesomeIcon)`
  margin-left: 10px;
  color: #b8b8b8;
`;

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
                <CustomLink
                  attachment
                  type="button"
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
                </CustomLink>
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
  const { fromAccount, toAccount } = email;

  const [isHoverFrom, setIsHoverFrom] = useState(false);
  const [isHoverTo, setIsHoverTo] = useState(false);
  const mouseEnter = iconArea =>
    iconArea === 'from' ? setIsHoverFrom(true) : setIsHoverTo(true);
  const mouseLeave = iconArea =>
    iconArea === 'from' ? setIsHoverFrom(false) : setIsHoverTo(false);

  const splitNamesIntoArray = account => account.name.split(/\s*;\s*/);
  const calculateAccountOtherNamesNumber = account =>
    splitNamesIntoArray(account).length - 1;

  const trimNamesInitials = account => {
    const firstAccountNames = splitNamesIntoArray(account)[0].split(' ');

    return firstAccountNames.length === 1
      ? firstAccountNames[0].charAt(0).toUpperCase()
      : firstAccountNames[0].charAt(0).toUpperCase() +
          firstAccountNames[firstAccountNames.length - 1]
            .charAt(0)
            .toUpperCase();
  };

  const activeEmailThread = threads.filter(
    thread => thread.id === activeThread
  );
  const dateReceived = activeEmailThread[0].threadProperties.dateReceived;
  const date = dateReceived
    ? moment(dateReceived).format('dddd D MMM YYYY')
    : moment().format('dddd D MMM YYYY');

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
          onlyInitials={trimNamesInitials(fromAccount)}
          role={fromAccount.role}
          email={fromAccount.email}
          triggerText={
            <FromAccountInitials>
              {trimNamesInitials(fromAccount)}
            </FromAccountInitials>
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
          <EmailFieldInnerContainer
            onMouseOver={() => mouseEnter('from')}
            onMouseLeave={() => mouseLeave('from')}
          >
            <EmailCard
              onlyInitials={trimNamesInitials(fromAccount)}
              name={fromAccount.name}
              role={fromAccount.role}
              email={fromAccount.email}
              triggerText={
                <NameLink isHover={isHoverFrom}>
                  {fromAccount.name || ' '}
                  <Icon icon={faChevronDown} />
                </NameLink>
              }
              onMouseOver={() => mouseEnter('from')}
              onMouseLeave={() => mouseLeave('from')}
            />
          </EmailFieldInnerContainer>
        </EmailField>
        <EmailField>
          <p>To: </p>
          <EmailFieldInnerContainer
            onMouseOver={() => mouseEnter('to')}
            onMouseLeave={() => mouseLeave('to')}
          >
            <EmailCard
              name={toAccount.name}
              onlyInitials={trimNamesInitials(toAccount)}
              email={toAccount.email}
              role={toAccount.role}
              otherAccountsNumber={calculateAccountOtherNamesNumber(toAccount)}
              triggerText={
                <NameLink isHover={isHoverTo}>
                  {toAccount.name || ' '}
                  <Icon icon={faChevronDown} />
                </NameLink>
              }
              onMouseOver={() => mouseEnter('to')}
              onMouseLeave={() => mouseLeave('to')}
            />
          </EmailFieldInnerContainer>
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
    <CustomLink
      type="button"
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
    >
      {props.children}
    </CustomLink>
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
          marginBottom: 30,
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
