import React, { PureComponent } from 'react';
import { BrowserRouter, Route, Redirect, Link } from 'react-router-dom';
import styled, { css } from 'react-emotion';

import Inbox from './pages/Inbox';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100vh',
});

const Sidebar = styled('div')({
  flex: 0,
  height: '100%',
  background: '#161415',
});

const StyledLink = styled(Link)(
  {
    display: 'block',
    padding: '20px 40px',
    textDecoration: 'none',
    letterSpacing: '1.5px',
    fontSize: 18,
  },
  props => ({
    fontWeight: props.isMatch ? 'bold' : 'normal',
    color: props.isMatch ? '#FFF' : '#C1C1C1',
  })
);

function SidebarLink({ to, children }) {
  return (
    <Route path={to}>
      {({ match }) => (
        <StyledLink to={to} isMatch={!!match}>
          {children}
        </StyledLink>
      )}
    </Route>
  );
}

class App extends PureComponent {
  render() {
    return (
      <BrowserRouter>
        <Container>
          <Sidebar>
            <div
              className={css({
                height: 80,
                width: '100%',
                backgroundColor: '#1D1B1C',
              })}
            />
            <SidebarLink className={css({ marginTop: 30 })} to="/inbox">
              Inbox
            </SidebarLink>
            <SidebarLink to="/accounts">Accounts</SidebarLink>
            <SidebarLink to="/contacts">Contacts</SidebarLink>
            <SidebarLink to="/web">Web</SidebarLink>
            <SidebarLink to="/files">Files</SidebarLink>
          </Sidebar>

          <div className={css({ flex: 1 })}>
            <Redirect from="/" to="/inbox" />
            <Route path="/inbox" component={Inbox} />
          </div>
        </Container>
      </BrowserRouter>
    );
  }
}

export default App;
