const EMAILS = [
  {
    id: '0',
    subject: 'Welcome on board!',
    from: 'Arther Ardent',
    emails: [
      {
        subject: 'Welcome on board!',
        from: {
          name: 'Arther Ardent',
          photoUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
        },
        id: 'fa59b235-184f-40ba-aae7-daaf48689d22',
        timestamp: '2018-02-20:15:31.000Z',
        body: `Hello Ana,\n\nThank you for helping out with the conference organisation. Great to have you on board!\n\nWe are currently...`,
      },
    ],
  },
  {
    id: '1',
    subject: 'Welcome drink',
    from: 'Peter Pollard',
    emails: [
      {
        subject: 'Welcome drinks',
        from: {
          name: 'Peter Pollard',
          photoUrl: 'https://randomuser.me/api/portraits/men/79.jpg',
        },
        id: '6e42899c-b868-4fa6-af3c-5a6bdf2ef66f',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Ana',
      },
      {
        subject: 'Welcome drinks',
        from: {
          name: 'Me',
          photoUrl: 'https://randomuser.me/api/portraits/women/83.jpg',
        },
        id: '6e42899c-3868-4fa6-af3c-5a6bdf2ef66f',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Peter',
      },
      {
        subject: 'Welcome drinks',
        from: {
          name: 'Me',
          photoUrl: 'https://randomuser.me/api/portraits/women/83.jpg',
        },
        id: '6e42899c-3868-5fa6-af3c-5a6bdf2ef66f',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Peter',
      },
      {
        subject: 'Welcome drinks',
        from: {
          name: 'Me',
          photoUrl: 'https://randomuser.me/api/portraits/women/83.jpg',
        },
        id: '6e42899c-3868-6fa6-af3c-5a6bdf2ef66f',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Peter',
      },
      {
        subject: 'Welcome drinks',
        from: {
          name: 'Me',
          photoUrl: 'https://randomuser.me/api/portraits/women/83.jpg',
        },
        id: '6e42899c-3868-7fa6-af3c-5a6bdf2ef66f',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Peter',
      },
    ],
  },
  {
    id: '2',
    subject: 'URGENT: Processed payments',
    from: 'Bea Bright',
    emails: [
      {
        subject: 'URGENT: Processed payments',
        from: {
          name: 'Bea Bright',
        },
        id: '5bdebcf9-7911-4757-befd-d2bc86f0ffdb',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Ana',
        replies: [
          {
            id: 5,
            type: 'reply',
            message: "I'm really sorry that can't be done",
          },
          { id: 6, type: 'forward', message: 'hey you should see this' },
        ],
      },
    ],
  },
  {
    id: '3',
    subject: 'Cool pic',
    from: 'Danielle Day',
    emails: [
      {
        subject: 'Cool pic',
        from: {
          name: 'Danielle Day',
          photoUrl: 'https://randomuser.me/api/portraits/women/67.jpg',
        },
        id: '261ef797-4b88-4c60-94db-7e4ab31682e8',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Check this out! Maybe we could use it for a flyer ;)',
      },
    ],
  },
  {
    id: '4',
    subject: 'Refund participant',
    from: 'Geoff Dave',
    emails: [
      {
        subject: 'Refund participant',
        from: {
          name: 'Geoff Dave',
        },
        id: '54476574-cc91-4e9a-b366-424b0aaed34d',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Ana',
      },
    ],
  },
  {
    id: '5',
    subject: 'Suspicious Activity',
    from: 'MoneyTransfer',
    emails: [
      {
        subject: 'Suspicious Activity',
        from: {
          name: 'MoneyTransfer',
        },
        id: 'ec705f8a-9492-4ab4-8768-f979bbdba760',
        timestamp: '2018-02-20:15:31.000Z',
        body: 'Hello Ana',
      },
    ],
  },
];

export function getThread(id) {
  return EMAILS.find(thread => thread.id === id);
}

export function getEmail(id) {
  return EMAILS.find(email => email.id === id);
}

export function getAllEmails() {
  return EMAILS;
}
