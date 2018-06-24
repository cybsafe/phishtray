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
  flexBasis: 320,
  backgroundColor: '#1B87EC',
  minHeight: '100%',
});

const EmailContainer = styled('div')({
  flex: 1,
});

export default class Inbox extends Component {
  render() {
    const { match } = this.props;
    const emails = getAllEmails();

    return (
      <Container>
        <EmailList>
          {emails.map(email => <EmailListItem key={email.id} email={email} />)}
        </EmailList>
        <EmailContainer>
          <Route path={`${match.url}/:emailId`} component={EmailDetail} />
        </EmailContainer>
      </Container>
    );
  }
}
