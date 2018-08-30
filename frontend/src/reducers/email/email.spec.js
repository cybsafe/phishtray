import * as emailApi from '../../api/exercise';
import { markEmailAsOpened } from './';

describe('email state', () => {
  beforeEach(() => {
    emailApi.createAction = jest.fn(); // eslint-disable-line import/namespace
  });

  describe('Given an email', () => {
    let email;

    beforeEach(() => {
      email = {
        id: '345',
      };
    });

    describe('When it is opened after 30 seconds', () => {
      let dispatch;
      let getState;
      const timer = 30;

      beforeEach(() => {
        dispatch = jest.fn();
        getState = jest
          .fn()
          .mockImplementation(() => ({ exercise: { timer } }));
        markEmailAsOpened(email)(dispatch, getState);
      });

      it('should send the email open action to the api with the email associstation and time in milliseconds', () => {
        expect(emailApi.createAction).toHaveBeenCalledWith(
          'email_open',
          { exerciseEmail: email.id },
          timer * 1000
        );
      });
    });
  });
});
