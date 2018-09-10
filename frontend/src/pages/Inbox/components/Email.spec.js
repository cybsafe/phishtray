import React from 'react';
import renderer from 'react-test-renderer';
import { EmailComponent as Email } from './Email';

describe('<Email />', () => {
  let props;

  beforeEach(() => {
    props = {
      markEmailAsOpened: jest.fn().mockImplementation(() => Promise.resolve()),
    };
  });

  describe('Given an email', () => {
    beforeEach(() => {
      props.email = {
        subject: 'Welcome on board!',
        from: {
          name: 'Arther Ardent',
          photoUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
          email: 'a.ardent@email.com',
          role: 'MD',
        },
        id: 'fa59b235-184f-40ba-aae7-daaf48689d22',
        timestamp: '2018-02-20:15:31.000Z',
        body: `Hello,\n\nThank you for helping out with the conference organisation. Great to have you on board!\n\nWe are about to make the pay run and need your bank details...\n\nThanks, Arther`,
      };
    });

    describe('When it is rendered', () => {
      beforeEach(() => {
        renderer.create(<Email {...props} />);
      });

      it('should call the `markEmailAsOpened` callback', () => {
        expect(props.markEmailAsOpened).toHaveBeenCalledWith(props.email);
      });
    });
  });
});
