import React, { Component, Fragment } from 'react';
import { BrowserRouter, Switch, Route, Redirect, Link } from 'react-router-dom';
import { Provider } from 'react-redux';

import { store, persistor } from './redux';

import { PersistGate } from 'redux-persist/integration/react';
import PhishTray from './routes';

export default () => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <PhishTray />
    </PersistGate>
  </Provider>
);
