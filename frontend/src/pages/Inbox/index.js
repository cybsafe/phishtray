import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled from 'react-emotion';

import { getAllEmails, getThread } from '../../data/threads';

import EmailChain from './components/EmailChain';
import EmailListItem from './components/EmailListItem';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
});

const EmailList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1B87EC',
  minHeight: '100%',
});

const EmailContainer = styled('div')({
  flex: 1,
  overflow: 'auto',
  paddingBottom: 80,
});

class Inbox extends Component {
  state = {
    threads: getAllEmails(),
    thread: getThread(this.props.location.pathname.substring(7)),
  };

  emailRead = emailId => {
    const updatedEmails = this.state.threads.map(
      email => (emailId === email.id ? (email.read = true) : email)
    );

    this.setState({ updatedEmails });
  };

  emailRender = () => {
    this.setState({
      thread: getThread(this.props.location.pathname.substring(7)),
    }),
      this.emailReRender;
  };

  emailAdd = email => {
    const thread = { ...this.state.thread };
    const addedEmail = [...this.state.thread.emails, email];
    thread.emails = addedEmail;

    this.setState({ thread: thread });
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
              emailRender={this.emailRender}
            />
          ))}
        </EmailList>
        <EmailContainer>
          <Route
            path={`${match.url}/:emailId`}
            render={() => {
              return (
                <EmailChain
                  thread={this.state.thread}
                  emailAdd={this.emailAdd}
                />
              );
            }}
          />
        </EmailContainer>
      </Container>
    );
  }
}

export default Inbox;
