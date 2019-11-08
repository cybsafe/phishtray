import React from 'react';
import styled, { css } from 'react-emotion';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUsers } from '@fortawesome/free-solid-svg-icons';

import { Tooltip } from 'carbon-components-react';

type Props = {
  name: string,
  email: string,
  triggerText: React.Node,
  role?: string,
  direction?: string,
  onlyInitials: string,
};

const AccountIconsContainer = styled('div')({
  display: 'flex',
  alignItems: 'center',
});

const FromAccountInitials = styled('div')({
  width: 80,
  height: 80,
  borderRadius: '50%',
  backgroundColor: '#1B87EC',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  color: 'white',
  fontSize: '2.5rem',
});

const P = styled('p')({
  fontSize: '1.5rem',
  color: '#B8B8B8',
  marginLeft: '10px',
});

const Icon = styled(FontAwesomeIcon)({
  marginLeft: '4px',
  fontSize: '16px',
});

const EmailCard = (props: Props) => {
  const {
    triggerText,
    direction,
    onlyInitials,
    role,
    email,
    name,
    otherAccountsNumber,
  } = props;
  return (
    <Tooltip
      showIcon={false}
      triggerText={triggerText}
      direction={direction ? direction : 'bottom'}
      otherAccountsNumber={otherAccountsNumber}
    >
      <AccountIconsContainer>
        <FromAccountInitials>{onlyInitials}</FromAccountInitials>
        {!!otherAccountsNumber && (
          <P>
            +{otherAccountsNumber}
            <Icon icon={faUsers} />
          </P>
        )}
      </AccountIconsContainer>
      <h2>{name}</h2>
      <br />
      {role && <p className="bx--tooltip__label">{role}</p>}
      <br />
      <p className={css({ color: '#B8B8B8' })}>
        {email ? `E: ${props.email}` : ''}
      </p>
    </Tooltip>
  );
};

export default EmailCard;
