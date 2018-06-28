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
    fontWeight: props.isRead === true ? 'normal' : 'bold',

    '&::before': {
      fontSize: 9,
      fontWeight: 'lighter',
      paddingLeft: 2,
      paddingRight: 2,
      content: props.isRead === true ? `''` : `'!'`,
      visibility: props.isRead === true ? 'hidden' : 'visible',
      backgroundColor: 'red',
      borderRadius: 20,
      color: 'white',
    },
  })
);

const Text = styled('div')(
  {
    color: '#fff',
    letterSpacing: '1.2px',
    textDecoration: 'none',
  },

  props => ({
    opacity: props.isSelected ? 1 : 0.7,
  })
);

export default function EmailListItem({ thread, emailRead }) {
  const handleClick = () => {
    emailRead(thread.id);
  };

  return (
    <Route path={`/inbox/${thread.id}`}>
      {({ match }) => (
        <Link
          onClick={handleClick}
          to={`/inbox/${thread.id}`}
          className={css({ textDecoration: 'none', display: 'block' })}
        >
          <Container isSelected={!!match} isRead={thread.read}>
            <Text
              isRead={thread.read}
              isSelected={!!match}
              className={css({
                fontSize: 18,
                lineHeight: '21px',
                marginBottom: 10,
              })}
            >
              {thread.subject}
            </Text>
            <Text isSelected={!!match} isRead={thread.read}>
              {thread.from}
            </Text>
          </Container>
        </Link>
      )}
    </Route>
  );
}
