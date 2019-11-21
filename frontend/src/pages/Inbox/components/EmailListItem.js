import React from 'react';
import { Route, Link } from 'react-router-dom';
import { connect } from 'react-redux';
import styled, { css } from 'react-emotion';

import { logAction } from '../../../utils';
import actionTypes from '../../../config/actionTypes';
import { markThreadAsActive } from '../../../actions/exerciseActions';

const Container = styled('div')(
  {
    padding: '30px',
    paddingLeft: '14px',
    borderLeft: '6px solid transparent',
  },
  props => ({
    backgroundColor: props.isSelected ? '#1C8BF4' : 'inherit',
    borderLeftColor: props.isSelected ? '#f4c760' : 'transparent',
  })
);

const Text = styled('div')(
  {
    color: '#fff',
    letterSpacing: '1.2px',
    textDecoration: 'none',
  },
  props => ({
    fontWeight: !props.isRead ? 'bold' : 'normal',
    opacity: !props.isRead ? 1 : 0.7,
  })
);

function EmailListItem({ email, onOpenParams, markThreadAsActive }) {
  const { startTime, participantId } = onOpenParams;
  return (
    <Route path={`/inbox/${email.id}`}>
      {({ match }) => (
        <Link
          to={`/inbox/${email.id}`}
          className={css({ textDecoration: 'none', display: 'block' })}
          onClick={() => {
            markThreadAsActive(email.id);
            logAction({
              participantId,
              actionType: actionTypes.emailOpen,
              emailId: email.id,
              timestamp: new Date(),
              timeDelta: Date.now() - startTime,
            });
          }}
        >
          <Container isSelected={!!match}>
            <Text
              isRead={email.isRead}
              className={css({
                fontSize: 18,
                lineHeight: '21px',
                marginBottom: 10,
              })}
            >
              {email.subject}
            </Text>
            <Text isRead={email.isRead}>{email.fromAccount.name}</Text>
          </Container>
        </Link>
      )}
    </Route>
  );
}

export default connect(
  null,
  { markThreadAsActive }
)(EmailListItem);
