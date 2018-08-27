import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';
import { connect } from 'react-redux';
import { EMAIL_ACTION_TYPES } from '../constants/email_constants';

import {
  getThread,
  markThreadAsRead,
  postUserActions,
} from '../../../reducers/inbox';

import getElapsedTime from '../../../reducers/exercise';

import Email from './Email';

export class EmailChain extends Component {
  componentDidMount() {
    const { thread } = this.props;
    if (!thread.idRead) {
      this.props.markThreadAsRead(thread.id);
      this.props.postUserActions(
        new Date() - this.props.elapsedTime,
        thread,
        EMAIL_ACTION_TYPES.EMAIL_OPEN
      );
    }
  }

  componentDidUpdate(prevProps) {
    const { thread: oldThread } = prevProps;
    const { thread: newThread } = this.props;
    if (newThread.id !== oldThread.id && !newThread.isRead) {
      this.props.markThreadAsRead(newThread.id);
      this.props.postUserActions(
        new Date() - this.props.elapsedTime,
        newThread,
        EMAIL_ACTION_TYPES.EMAIL_OPEN
      );
    }
  }
  onEmailResponse = val => {
    const { thread } = this.props;
    console.log(val);
    this.props.postUserActions(
      new Date() - this.props.elapsedTime,
      thread,
      val
    );
  };

  render() {
    const { thread } = this.props;
    return thread.emails.map(email => (
      <Fragment key={email.id}>
        <Email clicked={val => this.onEmailResponse(val)} email={email} />
        <hr
          className={css({
            width: '100%',
          })}
        />
      </Fragment>
    ));
  }
}

export default connect(
  (state, props) => ({
    thread: getThread(state, { threadId: props.match.params.emailId }),
    elapsedTime: getElapsedTime(state.exercise.startTime),
  }),
  {
    markThreadAsRead: markThreadAsRead,
    postUserActions: postUserActions,
  }
)(EmailChain);
