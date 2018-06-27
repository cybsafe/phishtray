import React, { Component } from 'react';

import { getThread } from '../../../data/emails';
import Email from './Email';

//@TODO scrollbar for content
export default class EmailChain extends Component {
  render() {
    const { match } = this.props;
    const {
      params: { emailId },
    } = match;
    const thread = getThread(emailId);
    return thread.emails.map(email => <Email key={email.id} email={email} />);
  }
}
