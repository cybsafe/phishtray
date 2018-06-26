import React from 'react';
import { Route, Link } from 'react-router-dom';
import styled, { css } from 'react-emotion';

const Container = styled('div')(
  {
    padding: '30px',
    paddingLeft: '14px',
    borderLeft: '6px solid transparent',
  },
  props => ({
    backgroundColor: props.isSelected ? '#1C8BF4' : 'inherit',
    borderLeftColor: props.isSelected ? '#f4c760' : 'transparent',
    fontSize: props.isRead === true ? '12pt' : '20pt',
  })
);

const Text = styled('div')(
  {
    color: '#fff',
    letterSpacing: '1.2px',
    textDecoration: 'none',
  },

  props => ({
    fontWeight: props.isSelected ? 'bold' : 'normal',
    opacity: props.isSelected ? 1 : 0.7,
    '&::after': {
      content: props.isRead === true ? `''` : `'🤔'`,
    },
  })
);

export default function EmailListItem({ email, emailRead }) {
  const handleClick = () => {
    emailRead(email.id);
  };

  return (
    <Route path={`/inbox/${email.id}`}>
      {({ match }) => (
        <Link
          onClick={handleClick}
          to={`/inbox/${email.id}`}
          className={css({ textDecoration: 'none', display: 'block' })}
        >
          <Container isSelected={!!match} isRead={email.read}>
            <Text
              isRead={email.read}
              isSelected={!!match}
              className={css({
                fontSize: 18,
                lineHeight: '21px',
                marginBottom: 10,
              })}
            >
              {email.subject}
            </Text>
            <Text isSelected={!!match} isRead={email.read}>
              {email.from.name}
            </Text>
          </Container>
        </Link>
      )}
    </Route>
  );
}
