import React from 'react';
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
});

class MyPayment extends React.Component {
  state = {
    logged: {},
  };

  _changed = () => {
    this.state({
      logged: {},
    });
  };

  render() {
    const { logBrowserActions, actionTypes } = this.props;
    return (
      <Switch>
        <Route
          path="/congrats"
          render={() => (
            <LoginContainer>
              <h1>
                Thank you for reaching out to the Money Transfer service. We’ll
                be in touch shortly to arrange your payment.
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
                <TextInput
                  {...TextInputProps()}
                  onChange={event => {
                    if (!this.state.logged[event.target.id]) {
                      this.setState(
                        {
                          logged: {
                            ...this.state.logged,
                            [event.target.id]: true,
                          },
                        },
                        () =>
                          logBrowserActions({
                            actionType:
                              actionTypes.browserInputLoginCrendentials,
                            modifiedField: 'email',
                          })
                      );
                    }
                  }}
                />
              </FieldWrapper>
              <FieldWrapper>
                <Button
                  {...ButtonProps()}
                  onClick={() => {
                    logBrowserActions({
                      actionType: actionTypes.browserSubmittedDetails,
                    });
                    history.push('/congrats');
                  }}
                >
                  Next
                </Button>
              </FieldWrapper>
              <FieldWrapper>Having trouble logging in?</FieldWrapper>
              <FieldWrapper>
                <Button
                  {...ButtonAlternateProps()}
                  onClick={() =>
                    logBrowserActions({
                      actionType: actionTypes.browserUserSignUp,
                    })
                  }
                >
                  Sign Up
                </Button>
              </FieldWrapper>
            </LoginContainer>
          )}
        />
      </Switch>
    );
  }
}

export default MyPayment;
