import React from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { useSelector } from 'react-redux';
import { getAllContacts } from '../../data/contacts';

import ContactDetail from './components/ContactDetail';
import ContactListItem from './components/ContactListItem';
import actionTypes from '../../config/actionTypes';
import { logAction } from '../../utils';
import withErrorBoundary from '../../errors/ErrorBoundary';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
});

const ContactList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1969B8',
  minHeight: '100%',
});

const ContactsContainer = styled('div')({
  flex: 1,
  paddingBottom: '80px',
});

function NoMatch() {
  return (
    <div
      className={css({
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        letterSpacing: '1.2px',
        fontSize: '1.25rem',
        color: '#333',
      })}
    >
      This is your organisation info.
    </div>
  );
}

function Contacts({ match }) {
  const participantId = useSelector(state => state.exercise.participant);
  const startTime = useSelector(state => state.exercise.startTime);

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

export default withErrorBoundary(Contacts);
