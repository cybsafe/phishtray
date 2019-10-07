import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import {
  markThreadAsRead,
  markThreadAsInactive,
  markThreadAsDeleted,
  setSelectedReply,
} from '../../../actions/exerciseActions';
import { getThread } from '../../../selectors/exerciseSelectors';
import { showWebpage } from '../../../actions/uiActions';
import { addFile } from '../../../actions/fileManagerActions';
import actionTypes from '../../../config/actionTypes';
import Email from './Email';
import ActionLinkwithClick from '../../../components/ActionLink/ActionLinkwithClick';

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
        // to="#reply_options"
        data={{
          ...onReplyParams,
          actionType: actionTypes.emailReply,
        }}
        title="Reply"
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

export class EmailChain extends Component {
  componentDidMount() {
    const { thread } = this.props;
    if (thread && !thread.idRead) {
      this.props.markThreadAsRead(thread.id);
    }
  }

  componentDidUpdate(prevProps) {
    const { thread: oldThread } = prevProps;
    const { thread: newThread } = this.props;
    if (newThread.id !== oldThread.id && !newThread.isRead) {
      this.props.markThreadAsRead(newThread.id);
    }
  }

  render() {
    const { thread } = this.props;
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
          markThreadAsDeleted={this.props.markThreadAsDeleted}
          markThreadAsInactive={this.props.markThreadAsInactive}
          threadId={thread.id}
          onReplyParams={{
            startTime: this.props.startTime,
            participantId: this.props.participantId,
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
                addFile={this.props.addFile}
                markThreadAsDeleted={this.props.markThreadAsDeleted}
                showWebpage={this.props.showWebpage}
                onReplyParams={{
                  startTime: this.props.startTime,
                  participantId: this.props.participantId,
                  emailId: email.id,
                }}
                setSelectedReply={this.props.setSelectedReply}
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
}

export default connect(
  (state, props) => ({
    thread: getThread(state, { threadId: props.match.params.emailId }),
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
  }),
  {
    markThreadAsRead,
    markThreadAsInactive,
    showWebpage,
    addFile,
    markThreadAsDeleted,
    setSelectedReply,
  }
)(EmailChain);
