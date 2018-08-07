import { combineReducers } from 'redux';
import exercise from './exercise';
import inbox from './inbox';

const rootReducer = combineReducers({
  exercise,
  inbox,
});
export default rootReducer;
