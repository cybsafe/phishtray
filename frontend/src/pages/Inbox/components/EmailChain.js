import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';
import { connect } from 'react-redux';

import { getThread, markThreadAsRead } from '../../../reducers/inbox';

import Email from './Email';

export class EmailChain extends Component {
  componentDidMount() {
    const { thread } = this.props;
    if (!thread.idRead) {
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
    return thread.emails.map(email => (
      <Fragment key={email.id}>
        <Email email={email} />
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
  }),
  { markThreadAsRead }
)(EmailChain);
