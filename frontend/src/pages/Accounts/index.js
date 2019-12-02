import React from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { useSelector } from 'react-redux';
import { getAllAccounts } from '../../data/accounts';
import AccountDetail from './components/AccountDetail';
import AccountListItem from './components/AccountListItem';
import { logAction } from '../../utils';
import actionTypes from '../../config/actionTypes';

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

export default Accounts;
