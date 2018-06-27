import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import format from 'date-fns/format';
import Markdown from 'react-remarkable';

import { getAccount } from '../../../data/accounts';

const ActionLink = styled('a')({
  marginRight: 20,
  textDecoration: 'none',
  color: '#B8B8B8',
  fontWeight: 'bold',
  letterSpacing: '1.1px',
});

const BodyContainer = styled('div')({
  maxWidth: 880,
  margin: '0 auto',
  padding: '0 40px',
});

const Spacer = styled('div')({
  marginTop: 40,
  color: '#666',
  '& p': {
    marginBottom: 20,
    fontSize: 20,
  },
});

function AccountInfo({ account }) {
  return (
    <div
      class="bx--structured-list-row"
    >
      <div class="bx--structured-list-td bx--structured-list-content--nowrap">
        {account.key}
      </div>
      <div class="bx--structured-list-td">
        {account.value}
      </div>

  </div>

  );
}

export default class Account extends Component {
  render() {
    const { match } = this.props;
    const {
      params: { id },
    } = match;
    const account = getAccount(id);

    return (
      <BodyContainer>
        <h3
          className={css({
            marginTop: 40,
            fontSize: 40,
            color: '#333',
            letterSpacing: '1.2px',
          })}
        >
          {account.name}
        </h3>

        <Spacer/>
        <section class="bx--structured-list">
          {account.data.map(account => <AccountInfo account={account} />)}
        </section>

      </BodyContainer>
    );
  }
}
