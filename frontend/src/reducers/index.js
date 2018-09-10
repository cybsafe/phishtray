import { combineReducers } from 'redux';
import email from './email';
import exercise from './exercise';
import inbox from './inbox';

const rootReducer = combineReducers({
  email,
  exercise,
  inbox,
});
export default rootReducer;
