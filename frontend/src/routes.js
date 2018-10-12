import React, { Component } from 'react';
import { BrowserRouter, Switch, Route, Redirect, Link } from 'react-router-dom';
import styled, { css, cx } from 'react-emotion';
import { connect } from 'react-redux';
import Inbox from './pages/Inbox';
import Accounts from './pages/Accounts';
import Exercise from './pages/Exercise';
import Header from './components/Header';
import FileManager from './pages/FileManager';
import Web from './pages/Web';
import Afterward from './pages/Afterward';
import WebBrowser from './components/WebBrowser';
import { getHeaderText } from './utils';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  minHeight: '100%',
  height: '100%',
});

const WelcomeContainer = styled('div')({
  display: 'flex',
  alignItems: 'center',
  flexDirection: 'column',
  height: '100%',
  backgroundColor: '#fff',
  boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)',
  padding: '10rem 1rem 1rem',
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

const DefaultLayout = ({ children, renderProps }) => (
  <div
    className={css({
      height: '100%',
      minHeight: '100%',
      overflow: 'hidden',
      backgroundColor: '#f5f7fa',
    })}
  >
    <Header renderProps={renderProps} />
    <Container>
      <Sidebar>
        <SidebarLink className={css({ marginTop: 30 })} to="/inbox">
          Inbox
        </SidebarLink>
        <SidebarLink to="/contacts">Contacts</SidebarLink>
        <SidebarLink to="/accounts">Accounts</SidebarLink>
        <SidebarLink to="/web">Web</SidebarLink>
        <SidebarLink to="/files">Files</SidebarLink>
      </Sidebar>
      <div className={css({ flex: 1 })}>{children}</div>
    </Container>
  </div>
);

const Welcome = () => (
  <WelcomeContainer>
    <h1>Welcome to PhishTray</h1>
  </WelcomeContainer>
);

const PrivateRoute = ({ component: Component, isAllowed, ...rest }) => (
  <Route
    {...rest}
    render={props => {
      if (isAllowed)
        document.title = `Phishtray | ${getHeaderText(props.match.path)}`;
      return isAllowed ? (
        <DefaultLayout renderProps={props}>
          <Component {...props} />
        </DefaultLayout>
      ) : (
        <Redirect
          to={{
            pathname: '/welcome',
            state: { from: props.location },
          }}
        />
      );
    }}
  />
);

class PhishTray extends Component {
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
          <Switch>
            <Route exact path="/welcome" component={Welcome} />
            <Route path="/welcome/:exerciseUuid" component={Exercise} />
            <Route path="/afterward" component={Afterward} />
            <PrivateRoute
              exact
              path="/"
              isAllowed={this.props.isAllowed}
              component={Inbox}
            />
            <PrivateRoute
              path="/inbox"
              isAllowed={this.props.isAllowed}
              component={Inbox}
            />
            <PrivateRoute
              path="/accounts"
              isAllowed={this.props.isAllowed}
              component={Accounts}
            />
            <PrivateRoute
              path="/files"
              isAllowed={this.props.isAllowed}
              component={FileManager}
            />
            <PrivateRoute
              path="/web"
              isAllowed={this.props.isAllowed}
              component={Web}
            />
            <Route component={Welcome} />
          </Switch>
          <WebBrowser />
        </div>
      </BrowserRouter>
    );
  }
}

export default connect(
  state => ({
    isAllowed: state.exercise.id,
  }),
  {}
)(PhishTray);
