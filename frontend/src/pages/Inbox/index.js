import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled from 'react-emotion';

import { getAllEmails } from '../../data/emails';

import EmailDetail from './components/EmailDetail';
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
    emails: getAllEmails(),
  };

  emailRead = emailId => {
    const updatedEmails = this.state.emails.map(
      email => (emailId === email.id ? (email.read = true) : email)
    );

    this.setState({ updatedEmails });
  };

  render() {
    const { match } = this.props;

    return (
      <Container>
        <EmailList>
          {this.state.emails.map(email => (
            <EmailListItem
              key={email.id}
              email={email}
              emailRead={this.emailRead}
            />
          ))}
        </EmailList>
        <EmailContainer>
          <Route path={`${match.url}/:emailId`} component={EmailDetail} />
        </EmailContainer>
      </Container>
    );
  }
}

export default Inbox;
