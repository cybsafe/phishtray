import React, { Component } from 'react';
import { BrowserRouter, Route, Redirect, Link } from 'react-router-dom';
import { Button } from 'carbon-components-react';
import './App.css';

import Inbox from './pages/Inbox';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <ul>
            <li>
              <Link to="/inbox">Inbox</Link>
            </li>
            <li>
              <Link to="/accounts">Accounts</Link>
            </li>
            <li>
              <Link to="/contacts">Contacts</Link>
            </li>
            <li>
              <Link to="/web">Web</Link>
            </li>
            <li>
              <Link to="/files">Files</Link>
            </li>
          </ul>

          <hr />

          <Redirect from="/" to="/inbox" />
          <Route path="/inbox" component={Inbox} />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
