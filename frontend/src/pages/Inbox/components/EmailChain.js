import React, { Component } from 'react';

import { getThread } from '../../../data/emails';
import Email from './Email';

//@TODO scrollbar for content
//@TODO load emails into state so new ones can be added

// const { match } = this.props;
// const {
//   params: { emailId },
// } = match;

export default class EmailChain extends Component {
  state = {
    thread: getThread(this.props.match.params.emailId),
  };

  emailReply = email => {
    // const emailReply = [...this.state.thread, email];
    // this.setState({ emailReply });
    console.log(email);
  };

  render() {
    return this.state.thread.emails.map(email => (
      <Email key={email.id} email={email} emailReply={this.emailReply} />
    ));
  }
}
