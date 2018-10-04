// @flow
import React from 'react';
import styled from 'react-emotion';
import { Button as CarbonButton } from 'carbon-components-react';

export type Props = {
  type: string,
  content: string,
  onClick?: (*) => void,
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
    white-space: normal;
    line-height: 22px;
    height: auto;
    text-align: left;
    :hover {
      color: white;
      background: #ffb100;
    }
    div {
      max-width: 500px;
      height: auto;
      overflow: hidden;
    }
  }
`;

const Button = (props: Props) => (
  <ReplyButton onClick={props.onClick || {}}>
    <div>{props.content}</div>
  </ReplyButton>
);

export default Button;
