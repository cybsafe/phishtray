import React, { Component } from 'react';
import { Switch, Route, Link } from 'react-router-dom';

export default class MyOffice extends Component {
  render() {
    return (
      <Switch>
        <Route
          path="/test"
          render={() => (
            <div>
              <h1>Test page</h1>
            </div>
          )}
        />
        <Route
          path="/"
          render={() => (
            <div>
              <h1>Welcome to MyOffice</h1>
              <Link to="/test">Go here</Link>
            </div>
          )}
        />
      </Switch>
    );
  }
}
