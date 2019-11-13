import React from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';

import { connect } from 'react-redux';
import { getAllContacts } from '../../data/contacts';

import ContactDetail from './components/ContactDetail';
import ContactListItem from './components/ContactListItem';
import actionTypes from '../../config/actionTypes';
import { logAction } from '../../utils';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  minHeight: '100%',
});

const ContactList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1969B8',
  minHeight: '100%',
});

const ContactsContainer = styled('div')({
  flex: 1,
});

function NoMatch() {
  return (
    <div
      className={css({
        maxWidth: 880,
        margin: '0 auto',
        padding: '90px 90px',
      })}
    >
      <h3
        className={css({
          marginTop: 40,
          color: '#333',
          letterSpacing: '1.2px',
        })}
      >
        This is your secure credentials vault.
      </h3>
    </div>
  );
}

function Contacts({ match, participantId, startTime, ...params }) {
  const logActionsHandler = params => {
    return logAction({
      participantId: participantId,
      timeDelta: Date.now() - startTime,
      timestamp: new Date(),
      actionType: actionTypes.contactOpen,
      ...params,
    });
  };

  const contacts = getAllContacts();

  return (
    <Container>
      <ContactList>
        {contacts.map(contact => (
          <ContactListItem
            key={contact.id}
            contact={contact}
            logAction={params => logActionsHandler(params)}
          />
        ))}
      </ContactList>
      <ContactsContainer>
        <Switch>
          <Route path={`${match.url}/:id`} component={ContactDetail} />
          <Route component={NoMatch} />
        </Switch>
      </ContactsContainer>
    </Container>
  );
}

export default connect(
  state => ({
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
  }),
  null
)(Contacts);
