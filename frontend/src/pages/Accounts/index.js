import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';

import { getAllAccounts } from '../../data/accounts';

import AccountDetail from './components/AccountDetail';
import AccountListItem from './components/AccountListItem';

import { connect } from 'react-redux';
import { logAction } from '../../utils';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  minHeight: '100%',
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

class Accounts extends Component {
  logActionsHandler = params => {
    return logAction({
      participantId: this.props.participantId,
      timeDelta: Date.now() - this.props.startTime,
      timestamp: new Date(),
      actionType: 'account_open',
      ...params,
    });
  };

  render() {
    const { match } = this.props;
    const accounts = getAllAccounts();

    return (
      <Container>
        <AccountList>
          {accounts.map(account => (
            <AccountListItem
              key={account.id}
              account={account}
              logAction={params => this.logActionsHandler(params)}
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
}

export default connect(
  state => ({
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
  }),
  {}
)(Accounts);
