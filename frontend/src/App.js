import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Redirect, Link } from 'react-router-dom';
import styled, { css } from 'react-emotion';

import Inbox from './pages/Inbox';
import Accounts from './pages/Accounts';
import Header from './components/Header';
import FileManager from './pages/file-manager';

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

const StyledLink = styled(Link)(
  {
    display: 'block',
    padding: '20px 30px',
    textDecoration: 'none',
    letterSpacing: '1.5px',
    fontSize: 18,
  },
  props => ({
    fontWeight: props.isMatch ? 'bold' : 'normal',
    color: props.isMatch ? '#FFF' : '#C1C1C1',
  })
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

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div
          className={css({
            height: '100%',
            minHeight: '100%',
            overflow: 'hidden',
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

            <div className={css({ flex: 1 })}>
              <Switch>
                <Route path="/inbox" component={Inbox} />
                <Route path="/accounts" component={Accounts} />
                <Route
                  exact
                  path="/"
                  render={() => <Redirect from="/" to="/inbox" />}
                />
                <Route path="/files" component={FileManager} />
                <Route
                  exact
                  path="/"
                  render={() => <Redirect from="/" to="/files" />}
                />
              </Switch>
            </div>
          </Container>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
