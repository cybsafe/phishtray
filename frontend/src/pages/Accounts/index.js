import React from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { useSelector } from 'react-redux';
import { getAllAccounts } from '../../data/accounts';
import AccountDetail from './components/AccountDetail';
import AccountListItem from './components/AccountListItem';
import { logAction } from '../../utils';
import actionTypes from '../../config/actionTypes';
import withErrorBoundary from '../../errors/ErrorBoundary';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
});

const AccountList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1969B8',
  minHeight: '100%',
});

const AccountContainer = styled('div')({
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
      This is your secure credentials vault.
    </div>
  );
}

function Accounts({ match }) {
  const startTime = useSelector(state => state.exercise.startTime);
  const participantId = useSelector(state => state.exercise.participant);

  const logActionsHandler = params => {
    return logAction({
      participantId: participantId,
      timeDelta: Date.now() - startTime,
      timestamp: new Date(),
      actionType: actionTypes.accountOpen,
      ...params,
    });
  };

  const accounts = getAllAccounts();

  return (
    <Container>
      <AccountList>
        {accounts.map(account => (
          <AccountListItem
            key={account.id}
            account={account}
            logAction={params => logActionsHandler(params)}
          />
        ))}
      </AccountList>
      <AccountContainer>
        <Switch>
          <Route path={`${match.url}/:id`} component={AccountDetail} />
          <Route component={NoMatch} />
        </Switch>
      </AccountContainer>
    </Container>
  );
}

export default withErrorBoundary(Accounts);
