import React from 'react';
import { Route, Link } from 'react-router-dom';
import styled, { css } from 'react-emotion';

const Container = styled('div')({
  padding: '30px 20px',
});

const Text = styled('div')(
  {
    color: '#fff',
    letterSpacing: '1.2px',
    textDecoration: 'none',
  },
  props => ({
    fontWeight: props.isSelected ? 'bold' : 'normal',
    opacity: props.isSelected ? 1 : 0.7,
  })
);

export default function EmailListItem({ email }) {
  return (
    <Route path={`/inbox/${email.id}`}>
      {({ match }) => (
        <Link
          to={`/inbox/${email.id}`}
          className={css({ textDecoration: 'none', display: 'block' })}
        >
          <Container isSelected={!!match}>
            <Text
              isSelected={!!match}
              className={css({ fontSize: 18, marginBottom: 10 })}
            >
              {email.subject}
            </Text>
            <Text isSelected={!!match}>{email.from.name}</Text>
          </Container>
        </Link>
      )}
    </Route>
  );
}
