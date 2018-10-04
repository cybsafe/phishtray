import React from 'react';
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
