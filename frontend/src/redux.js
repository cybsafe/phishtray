/* global process */
import { createStore, applyMiddleware, compose } from 'redux';
import reduxThunk from 'redux-thunk';
import { persistStore, persistReducer } from 'redux-persist';
import * as Sentry from '@sentry/browser';
import storage from 'redux-persist/lib/storage/session';

import reducer from './reducers';
import sentryMiddleware from './sentryMiddleware';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['exercise', 'fileManager'],
};

const persistedReducer = persistReducer(persistConfig, reducer);

const configureStore = initialState => {
  let middlewares = [reduxThunk];

  /* eslint-disable */
  const composeEnhancers =
    process.env.NODE_ENV !== 'production' &&
    typeof window === 'object' &&
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
      ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({})
      : compose;
  /* eslint-enable */

  if (process.env.NODE_ENV !== 'production') {
    const { createLogger } = require('redux-logger');
    const loggerMiddleware = createLogger({
      collapsed: true,
      duration: true,
    });
    middlewares.push(loggerMiddleware);
  }

  if (process.env.SENTRY_DSN) {
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      ignoreErrors: [
        'Network Error',
        'Not enough storage is available to complete this operation.',
      ],
    });
    middlewares.push(sentryMiddleware(Sentry));
  }

  const store = createStore(
    persistedReducer,
    initialState,
    composeEnhancers(applyMiddleware(...middlewares))
  );
  return store;
};

const store = configureStore();
const persistor = persistStore(store);
export { store, persistor };
