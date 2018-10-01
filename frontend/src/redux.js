/* global process */
import { createStore, applyMiddleware, compose } from 'redux';
import reduxThunk from 'redux-thunk';

import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage

import reducer from './reducers';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['exercise'],
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

  const store = createStore(
    // reducer,
    persistedReducer,
    initialState,
    composeEnhancers(applyMiddleware(...middlewares))
  );
  return store;
};

let store = configureStore();
let persistor = persistStore(store);
export { store, persistor };
// export default configureStore;
