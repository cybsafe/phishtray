/* global process */
import { createStore, applyMiddleware, compose } from 'redux';
import reduxThunk from 'redux-thunk';

import reducer from './reducers';

const configureStore = initialState => {
  let middlewares = [reduxThunk];

  /* eslint-disable */
  const serverData = window.__data__ || {};
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

  const store = createStore(
    reducer,
    initialState,
    composeEnhancers(applyMiddleware(...middlewares))
  );
  return store;
};

export default configureStore;
