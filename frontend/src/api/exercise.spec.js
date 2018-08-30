import { createAction } from './exercise';

describe('exercise API', () => {
  describe('Given an action', () => {
    const actionType = 'email_open';
    const associations = { exerciseEmail: '1234' };
    const timer = 1000;

    describe('When the action is to be sent to the API', () => {
      beforeEach(async () => {
        window.fetch = jest.fn().mockImplementation(() => Promise.resolve());
        await createAction(actionType, associations, timer);
      });

      afterEach(() => {
        jest.clearAllMocks();
      });

      it('should send the data to create the action', () => {
        const [endpoint, data] = window.fetch.mock.calls[0];
        expect(endpoint).toBe('/exercise/1/action/');
        expect(JSON.parse(data.body)).toEqual({
          milliseconds: timer,
          action: {
            type: actionType,
            associations,
          },
        });
      });
    });
  });
});
