import React, { useEffect } from 'react';
import { Route } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { useSelector } from 'react-redux';
import { InlineLoading } from 'carbon-components-react';
import {
  getThreads,
  getUnreadThreads,
} from '../../selectors/exerciseSelectors';
import EmailChain from './components/EmailChain';
import EmailListItem from './components/EmailListItem';
import withErrorBoundary from '../../errors/ErrorBoundary';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
});

const NoActiveMessage = styled('div')`
  justify-content: center;
  align-items: center;
  display: flex;
  height: 100%;
  color: #333;
  letter-spacing: 1.2px;
  font-size: 1.25rem;
`;

const EmailList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1B87EC',
  minHeight: '100%',
  overflow: 'auto',
  paddingBottom: '80px',
});

const EmailContainer = styled('div')({
  flex: 1,
  overflow: 'auto',
  paddingBottom: 80,
});

function Inbox({ match, history }) {
  const { startTime, activeThread } = useSelector(state => state.exercise);
  const participantId = useSelector(state => state.exercise.participant);
  const threads = useSelector(state => getThreads(state));
  const countUnread = useSelector(state => getUnreadThreads(state));

  useEffect(() => {
    if (Object.keys(match.params).length === 0 && activeThread !== '') {
      history.push(`/inbox/${activeThread}`);
    }
    //eslint-disable-next-line
  }, []);

  if (!threads) {
    return (
      <Container>
        <EmailList>
          <InlineLoading
            className={css({
              color: '#fff',
              justifyContent: 'center',
              marginTop: '20%',
              '& svg': { stroke: '#fff !important' },
            })}
            description="Loading"
          />
        </EmailList>
        <EmailContainer />
      </Container>
    );
  }

  return (
    <Container>
      <EmailList>
        {threads.map(thread => (
          <EmailListItem
            key={thread.id}
            email={thread}
            onOpenParams={{
              startTime: startTime,
              participantId: participantId,
            }}
          />
        ))}
      </EmailList>
      <EmailContainer>
        {activeThread === '' ? (
          <NoActiveMessage>
            You have {countUnread} unread email
            {countUnread !== 1 && 's'}
          </NoActiveMessage>
        ) : (
          <Route path={`${match.url}/:emailId`} component={EmailChain} />
        )}
      </EmailContainer>
    </Container>
  );
}

export default withErrorBoundary(Inbox);
