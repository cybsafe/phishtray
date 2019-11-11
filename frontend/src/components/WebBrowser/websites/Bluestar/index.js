import React from 'react';
import { Switch, Route } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { TextInput, Button, Checkbox, Icon } from 'carbon-components-react';
import { iconStarOutline } from 'carbon-icons';

import Bg from './assets/bg.png';

const LoginContainer = styled('div')({
  margin: '120px auto 0',
  padding: '42px 42px 36px',
  overflow: 'hidden',
  width: '80%',
  // maxWidth: '1500px',
  flexDirection: 'row',
  flex: 1,
  justifyContent: 'space-around',
  display: 'flex',
});

const LoginContainerImage = styled('div')({
  flex: 1,
});

const LoginContainerForm = styled('div')({
  maxWidth: '440px',
  width: '100%',
});

const FieldWrapper = styled('div')({
  padding: '12px 12px 23px',
  overflow: 'hidden',
  display: 'flex',
});

const LoginBanner = styled('div')({
  flex: 1,
  borderBottom: '1px solid #eaeced',
  display: 'flex',
  position: 'absolute',
  top: '70px',
  width: '100%',
  padding: '15px 0px ',
});

const LoginBannerText = styled('div')({
  textAlign: 'center',
  color: '#4285F4',
  flexGrow: 1,
  fontSize: '36px',
  fontWeight: '800',
  fontFamily: 'Open Sans',
  letterSpacing: '3.6px',
  lineHeight: '40px',
});

const LoginHeaderText = styled('h2')({
  color: '#4285F4',
  lineHeight: '40px',
  fontFamily: 'Open Sans',
  fontSize: '36px',
});

const TextInputProps = () => ({
  className: css({ display: 'flex' }),
  disabled: false,
  labelText: '',
});

const ButtonProps = () => ({
  className: css({ display: 'flex', flexGrow: 1 }),
  id: 'button',
  kind: 'primary',
});

class MyBluestar extends React.Component {
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
              <h1>Thanks for visiting Bluestar Technologies.</h1>
            </LoginContainer>
          )}
        />
        <Route
          path="/"
          render={({ history }) => (
            <div>
              <LoginBanner>
                <Icon
                  icon={iconStarOutline}
                  name="iconStart"
                  fill="#4285F4"
                  height="40px"
                  width="150px"
                  className={css({
                    position: 'absolute',
                  })}
                />
                <LoginBannerText>BlueStar Technologies</LoginBannerText>
              </LoginBanner>
              <LoginContainer>
                <LoginContainerImage>
                  <img src={Bg} alt="background" />
                </LoginContainerImage>
                <LoginContainerForm>
                  <FieldWrapper>
                    <LoginHeaderText>Login</LoginHeaderText>
                  </FieldWrapper>
                  <FieldWrapper>
                    <TextInput
                      {...TextInputProps()}
                      id="email"
                      disabled
                      placeholder="Email"
                      type="email"
                      value="geoff@bluestar.com"
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
                    <TextInput
                      {...TextInputProps()}
                      id="password"
                      placeholder="Password"
                      type="password"
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
                                modifiedField: 'password',
                              })
                          );
                        }
                      }}
                    />
                  </FieldWrapper>
                  <FieldWrapper>
                    <Checkbox
                      labelText="Remember Me"
                      onChange={value =>
                        logBrowserActions({
                          actionType: actionTypes.browserInputChange,
                          modifiedField: 'remember_me',
                          fieldValue: value,
                        })
                      }
                      id="checkbox-label-1"
                    />
                    <Button
                      {...ButtonProps()}
                      onClick={() => {
                        logBrowserActions({
                          actionType: actionTypes.browserSubmittedDetails,
                        });
                        history.push('/congrats');
                      }}
                    >
                      Login
                    </Button>
                  </FieldWrapper>
                </LoginContainerForm>
              </LoginContainer>
            </div>
          )}
        />
      </Switch>
    );
  }
}

export default MyBluestar;
