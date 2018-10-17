// @flow
import React from 'react';
import styled from 'react-emotion';
import { Button as CarbonButton } from 'carbon-components-react';

export type Props = {
  type: string,
  content: string,
  onClick?: (*) => void,
};

const ReplyButtonContainer = styled('div')({
  display: 'flex',
  justifyContent: 'center',
});

const ReplyButton = styled(CarbonButton)`
  &&& {
    color: #3d70b2;
    border-width: 1px;
    font-size: 1em;
    border-color: #3d70b2;
    background: white;
    border-radius: 16px;
    white-space: normal;
    line-height: 22px;
    height: auto;
    text-align: left;
    padding: 15px;
    margin: 1em 0;
    :hover {
      color: white;
      background: #3d70b2;
    }
    div {
      max-width: 500px;
      height: auto;
      overflow: hidden;
    }
  }
`;

const Button = (props: Props) => (
  <ReplyButtonContainer>
    <ReplyButton onClick={props.onClick || {}}>
      <div>{props.content}</div>
    </ReplyButton>
  </ReplyButtonContainer>
);

export default Button;
