import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import {
  markThreadAsRead,
  markThreadAsDeleted,
  setSelectedReply,
} from '../../../actions/exerciseActions';
import { getThread } from '../../../selectors/exerciseSelectors';
import { showWebpage } from '../../../actions/uiActions';
import { addFile } from '../../../actions/fileManagerActions';

import Email from './Email';

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
      thread.emails.map(email => (
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
      ))
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
    showWebpage,
    addFile,
    markThreadAsDeleted,
    setSelectedReply,
  }
)(EmailChain);
