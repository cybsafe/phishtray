import React, { Component, Fragment } from 'react';
import { BrowserRouter, Switch, Route, Redirect, Link } from 'react-router-dom';
import styled, { css, cx } from 'react-emotion';
import { Tile } from 'carbon-components-react';
import { Provider } from 'react-redux';

import { store, persistor } from './redux';

import Inbox from './pages/Inbox';
import Accounts from './pages/Accounts';
import Exercise from './pages/Exercise';
import Header from './components/Header';
import FileManager from './pages/FileManager';
import Web from './pages/Web';
import Afterward from './pages/Afterward';
import WebBrowser from './components/WebBrowser';

import { PersistGate } from 'redux-persist/integration/react';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  minHeight: '100%',
  height: '100%',
});

const Sidebar = styled('div')({
  flex: 0,
  flexBasis: '160px',
  height: '100%',
  background: '#161415',
});

const StyledLink = ({ isMatch, className, ...rest }) => (
  <Link
    className={cx([
      css({
        display: 'block',
        padding: '20px 30px',
        textDecoration: 'none',
        letterSpacing: '1.5px',
        fontSize: 18,
        fontWeight: isMatch ? 'bold' : 'normal',
        color: isMatch ? '#FFF' : '#C1C1C1',
      }),
      className,
    ])}
    {...rest}
  />
);

function SidebarLink({ to, children, ...rest }) {
  return (
    <Route path={to}>
      {({ match }) => (
        <StyledLink to={to} isMatch={!!match} {...rest}>
          {children}
        </StyledLink>
      )}
    </Route>
  );
}

const DefaultLayout = ({ children }) => (
  <Fragment>
    <div
      className={css({
        height: '100%',
        minHeight: '100%',
        overflow: 'hidden',
        backgroundColor: '#f5f7fa',
      })}
    >
      <Header />
      <Container>
        <Sidebar>
          <SidebarLink className={css({ marginTop: 30 })} to="/inbox">
            Inbox
          </SidebarLink>
          <SidebarLink to="/accounts">Accounts</SidebarLink>
          <SidebarLink to="/contacts">Contacts</SidebarLink>
          <SidebarLink to="/web">Web</SidebarLink>
          <SidebarLink to="/files">Files</SidebarLink>
        </Sidebar>
        <div className={css({ flex: 1 })}>{children}</div>
      </Container>
    </div>
  </Fragment>
);

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <BrowserRouter>
            <div
              className={css({
                height: '100%',
                minHeight: '100%',
                overflow: 'hidden',
              })}
            >
              <Switch>
                <Route
                  path="/inbox"
                  render={props => (
                    <DefaultLayout>
                      <Inbox {...props} />
                    </DefaultLayout>
                  )}
                />
                <Route
                  path="/accounts"
                  render={props => (
                    <DefaultLayout>
                      <Accounts {...props} />
                    </DefaultLayout>
                  )}
                />
                <Route
                  path="/files"
                  render={props => (
                    <DefaultLayout>
                      <FileManager {...props} />
                    </DefaultLayout>
                  )}
                />
                <Route
                  path="/web"
                  render={props => (
                    <DefaultLayout>
                      <Web {...props} />
                    </DefaultLayout>
                  )}
                />
                <Route path="/welcome/:exerciseUuid" component={Exercise} />
                <Route
                  path="/afterward"
                  render={() => (
                    <Tile>
                      <Afterward />
                    </Tile>
                  )}
                />
                <Route
                  exact
                  path="/"
                  render={() => <Redirect from="/" to="/inbox" />}
                />
                <Route component={DefaultLayout} />
              </Switch>
              <WebBrowser />
            </div>
          </BrowserRouter>
        </PersistGate>
      </Provider>
    );
  }
}

export default App;
