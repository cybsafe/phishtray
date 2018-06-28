import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled from 'react-emotion';

import { getAllEmails } from '../../data/threads';

import EmailChain from './components/EmailChain';
import EmailListItem from './components/EmailListItem';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  minHeight: '100%',
});

const EmailList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1B87EC',
  minHeight: '100%',
});

const EmailContainer = styled('div')({
  flex: 1,
});

class Inbox extends Component {
  state = {
    threads: getAllEmails(),
  };

  emailRead = emailId => {
    const updatedEmails = this.state.threads.map(
      email => (emailId === email.id ? (email.read = true) : email)
    );

    this.setState({ updatedEmails });
  };

  render() {
    const { match } = this.props;

    return (
      <Container>
        <EmailList>
          {this.state.threads.map(thread => (
            <EmailListItem
              key={thread.id}
              thread={thread}
              emailRead={this.emailRead}
            />
          ))}
        </EmailList>
        <EmailContainer>
          <Route path={`${match.url}/:emailId`} component={EmailChain} />
        </EmailContainer>
      </Container>
    );
  }
}

export default Inbox;
