import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';
import { connect } from 'react-redux';

import { getThread } from '../../../reducers/inbox';

import Email from './Email';

export class EmailChain extends Component {
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

export default connect((state, props) => ({
  thread: getThread(props.match.params.emailId)(state),
}))(EmailChain);
