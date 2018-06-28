import React from 'react';
import { css } from 'react-emotion';

import { Tooltip } from 'carbon-components-react';

type Props = {
  name: string,
  photoUrl: string,
  email: string,
  triggerText: React.Node,
  role?: string,
  direction?: string,
};

const EmailCard = (props: Props) => (
  <Tooltip
    showIcon={false}
    triggerText={props.triggerText}
    direction={props.direction ? props.direction : 'bottom'}
  >
    <img
      className={css({
        width: 80,
        height: 80,
        borderRadius: '50%',
        marginRight: 20,
      })}
      src={props.photoUrl}
      alt=""
    />
    <h2>{props.name}</h2>
    <br />
    {props.role && <p className="bx--tooltip__label">{props.role}</p>}
    <br />
    <p className={css({ color: '#B8B8B8' })}>
      {props.email ? `E: ${props.email}` : ''}
    </p>
  </Tooltip>
);

export default EmailCard;
