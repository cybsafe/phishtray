// @flow
import React from 'react';
import styled, { css } from 'react-emotion';
import { type Match } from 'react-router-dom';
import CopyButton from '../../../components/Button/CopyButton';
import { getAccount } from '../../../data/accounts';

type Props = {
  match: Match,
};

const BodyContainer = styled('div')({
  maxWidth: 880,
  margin: '0 auto',
  padding: '0 40px',
});

const Spacer = styled('div')({ height: 40 });

function AccountInfo({ credentials }) {
  return (
    <div className="bx--structured-list-row">
      <div className="bx--structured-list-td bx--structured-list-content--nowrap">
        {credentials.label}
      </div>
      <div className="bx--structured-list-td">{credentials.value}</div>
      <div className="bx--structured-list-td">
        <CopyButton copyText={credentials.value} />
      </div>
    </div>
  );
}

const Account = (props: Props) => {
  const { match } = props;
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

      <Spacer />
      <section className="bx--structured-list">
        {account.data.map(credentials => (
          <AccountInfo key={credentials.id} credentials={credentials} />
        ))}
      </section>
    </BodyContainer>
  );
};

export default Account;
