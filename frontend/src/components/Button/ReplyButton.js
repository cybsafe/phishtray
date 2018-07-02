// @flow
import React from 'react';
import styled from 'react-emotion';
import { Button as CarbonButton } from 'carbon-components-react';

export type Props = {
  type: string,
  content: string,
};

const ReplyButton = styled(CarbonButton)`
  &&& {
    color: #ffb100;
    border-width: 1px;
    font-size: 1em;
    margin: 1em;
    border-color: #ffb100;
    background: white;
    border-radius: 16px;
    :hover {
      color: white;
      background: #ffb100;
    }
  }
`;

const Button = (props: Props) => (
  <ReplyButton onClick={() => {}}>{props.content}</ReplyButton>
);

export default Button;
