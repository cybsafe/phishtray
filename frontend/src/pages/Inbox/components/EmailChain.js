import React, { Component, Fragment } from 'react';
import { css } from 'react-emotion';

import { getThread } from '../../../data/threads';
import Email from './Email';

export default class EmailChain extends Component {
  render() {
    const { match } = this.props;
    const {
      params: { emailId },
    } = match;
    const thread = getThread(emailId);
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
