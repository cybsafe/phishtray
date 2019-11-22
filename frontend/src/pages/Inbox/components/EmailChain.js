import React, { Fragment, createRef, useEffect } from 'react';
import { css } from 'react-emotion';
import { Redirect } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import {
  markThreadAsRead,
  markThreadAsInactive,
  markThreadAsDeleted,
  setSelectedReply,
} from '../../../actions/exerciseActions';
import { showWebpage } from '../../../actions/uiActions';
import { addFile } from '../../../actions/fileManagerActions';
import actionTypes from '../../../config/actionTypes';
import Email from './Email';
import ActionLinkwithClick from '../../../components/ActionLink/ActionLinkwithClick';

const repliesRef = createRef();

const onReplyPress = () =>
  repliesRef.current.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  });

function EmailActions({
  threadId,
  markThreadAsDeleted,
  onReplyParams,
  markThreadAsInactive,
}) {
  return (
    <div
      className={css({
        flexShrink: '0',
        display: 'flex',
        justifyContent: 'flex-end',
        paddingTop: '20px',
        paddingBottom: '20px',
        background: 'white',
      })}
    >
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: actionTypes.emailReply,
        }}
        title="Reply"
        onReplyPress={onReplyPress}
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: actionTypes.emailForward,
        }}
        title="Forward"
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: actionTypes.emailDelete,
        }}
        title="Delete"
        markThreadAsDeleted={markThreadAsDeleted}
        markThreadAsInactive={markThreadAsInactive}
        threadId={threadId}
        remove
        secondary={1}
      />
      <ActionLinkwithClick
        data={{
          ...onReplyParams,
          actionType: actionTypes.emailReport,
        }}
        title="Report"
        markThreadAsDeleted={markThreadAsDeleted}
        markThreadAsInactive={markThreadAsInactive}
        threadId={threadId}
        remove
      />
    </div>
  );
}

function EmailChain({ match }) {
  const threads = useSelector(state => state.exercise.threads);
  const thread = threads.filter(e => e.id === match.params.emailId)[0];
  const { startTime } = useSelector(state => state.exercise);
  const participantId = useSelector(state => state.exercise.participant);
  const dispatch = useDispatch();

  useEffect(() => {
    if (thread && !thread.idRead) {
      dispatch(markThreadAsRead(thread.id));
    }
  }, [thread, dispatch]);

  return thread ? (
    <div
      className={css({
        height: '100%',
        display: 'flex',
        boxSizing: 'border-box',
        flexDirection: 'column',
      })}
      key={thread.id}
    >
      <EmailActions
        markThreadAsDeleted={(...arg) => dispatch(markThreadAsDeleted(...arg))}
        markThreadAsInactive={(...arg) =>
          dispatch(markThreadAsInactive(...arg))
        }
        threadId={thread.id}
        onReplyParams={{
          startTime,
          participantId,
          emailId: thread.id,
        }}
      />
      <div
        className={css({
          flexGrow: 1,
          overflowY: 'auto',
        })}
      >
        {thread.emails.map(email => (
          <Fragment key={email.id}>
            <Email
              email={email}
              threadId={thread.id}
              addFile={(...arg) => dispatch(addFile(...arg))}
              markThreadAsDeleted={(...arg) =>
                dispatch(markThreadAsDeleted(...arg))
              }
              showWebpage={(...arg) => dispatch(showWebpage(...arg))}
              onReplyParams={{
                startTime,
                participantId,
                emailId: email.id,
              }}
              setSelectedReply={(...arg) => dispatch(setSelectedReply(...arg))}
              repliesRef={repliesRef}
            />
            <hr
              className={css({
                width: '100%',
              })}
            />
          </Fragment>
        ))}
      </div>
    </div>
  ) : (
    <Redirect to="/inbox" />
  );
}

export default EmailChain;
