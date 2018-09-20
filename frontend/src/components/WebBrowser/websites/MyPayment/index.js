import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { TextInput, Button } from 'carbon-components-react';

import Logo from './assets/logo.png';

const LoginContainer = styled('div')({
  margin: '120px auto 0',
  padding: '42px 42px 36px',
  overflow: 'hidden',
  width: '500px',
  border: '1px solid #eaeced',
  textAlign: 'center',
});

const FieldWrapper = styled('div')({
  padding: '12px 12px 23px',
  overflow: 'hidden',
  display: 'flex',
});

const TextInputProps = () => ({
  className: css({ display: 'flex' }),
  id: 'test2',
  type: 'email',
  placeholder: 'Email Address',
  disabled: false,
  onClick: () => console.log('onClick'),
  labelText: '',
});

const ButtonProps = () => ({
  className: css({ display: 'flex', flexGrow: 1 }),
  id: 'test2',
  kind: 'primary',
});

const ButtonAlternateProps = () => ({
  className: css({ display: 'flex', flexGrow: 1 }),
  id: 'test2',
  kind: 'secondary',
  onClick: () => console.log('onClick'),
});

export default class MyPayment extends Component {
  render() {
    return (
      <Switch>
        <Route
          path="/congrats"
          render={() => (
            <LoginContainer>
              <h1>
                Thank you for checking. Your recent transactions have been
                verified.
              </h1>
            </LoginContainer>
          )}
        />
        <Route
          path="/"
          render={({ history }) => (
            <LoginContainer>
              <img src={Logo} width={323} height={58} alt="logo" />
              <FieldWrapper>
                <TextInput {...TextInputProps()} />
              </FieldWrapper>
              <FieldWrapper>
                <Button
                  {...ButtonProps()}
                  onClick={() => history.push('/congrats')}
                >
                  Next
                </Button>
              </FieldWrapper>
              <FieldWrapper>Having trouble logging in?</FieldWrapper>
              <FieldWrapper>
                <Button {...ButtonAlternateProps()}>Sign Up</Button>
              </FieldWrapper>
            </LoginContainer>
          )}
        />
      </Switch>
    );
  }
}
