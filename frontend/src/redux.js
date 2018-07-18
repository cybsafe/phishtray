/* global process */
import { createStore, applyMiddleware } from 'redux';
import reduxThunk from 'redux-thunk';

import reducer from './reducers';

const configureStore = initialState => {
  let middlewares = [reduxThunk];

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
    applyMiddleware(...middlewares)
  );
  return store;
};

export default configureStore;
