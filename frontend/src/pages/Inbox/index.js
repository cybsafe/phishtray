import React, { PureComponent } from 'react';
import { Route, Link } from 'react-router-dom';

const Email = () => (
  <div />
);

export default class Inbox extends PureComponent {
  render() {
    const { match } = this.props;
    return (
      <div>
        <h2>Inbox</h2>
        <Route path={`${match.url}/:emailId`} component={Email} />
      </div>
    );
  }
}
