// @flow
import React, { Component } from 'react';
import styled from 'react-emotion';
import { Button as CarbonButton } from 'carbon-components-react';

export type Props = {
  type: string,
  content: string,
  subject: string,
  emailAdd: () => {},
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

export default class Button extends Component<Props> {
  handleClick = () => {
    this.props.emailAdd({
      subject: `${this.props.subject}`,
      from: {
        name: 'You',
        email: 'my@email.com',
      },
      id: '54476574-cc91-4e9a-b366-424b0aaed34d',
      timestamp: '2018-02-20:15:31.000Z',
      body: `${this.props.content}`,
    });
  };

  render() {
    return (
      <ReplyButton onClick={this.handleClick}>{this.props.content}</ReplyButton>
    );
  }
}
