import React from 'react';
import styled, { css } from 'react-emotion';

import { Tooltip } from 'carbon-components-react';

type Props = {
  name: string,
  photoUrl: string,
  email: string,
  triggerText: React.Node,
  role?: string,
  direction?: string,
  onlyInitials: string,
};

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

const FromAccountPhoto = styled('img')({
  width: 80,
  height: 80,
  borderRadius: '50%',
  marginRight: 20,
});

const EmailCard = (props: Props) => {
  const {
    triggerText,
    direction,
    photoUrl,
    onlyInitials,
    role,
    email,
    name,
  } = props;
  return (
    <Tooltip
      showIcon={false}
      triggerText={triggerText}
      direction={direction ? direction : 'bottom'}
    >
      {photoUrl ? (
        <FromAccountPhoto src={photoUrl} alt="" />
      ) : (
        <FromAccountInitials>{onlyInitials}</FromAccountInitials>
      )}
      <h2>{name}</h2>
      <br />
      {role && <p className="bx--tooltip__label">{role}</p>}
      <br />
      <p className={css({ color: '#B8B8B8' })}>{email ? `E: ${email}` : ''}</p>
    </Tooltip>
  );
};

export default EmailCard;
