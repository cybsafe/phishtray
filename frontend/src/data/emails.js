const EMAILS = [
  {
    subject: 'Welcome on board!',
    from: {
      name: 'Arther Ardent',
      photoUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
      email: 'a.ardent@email.com',
      role: 'MD',
    },
    id: 'fa59b235-184f-40ba-aae7-daaf48689d22',
    timestamp: '2018-02-20:15:31.000Z',
    body: `Hello Ana,\n\nThank you for helping out with the conference organisation. Great to have you on board!\n\nWe are currently...`,
  },
  {
    subject: 'Welcome drinks',
    from: {
      name: 'Peter Pollard',
      photoUrl: 'https://randomuser.me/api/portraits/men/79.jpg',
      email: 'peter.pollard1@email.com',
    },
    id: '6e42899c-b868-4fa6-af3c-5a6bdf2ef66f',
    timestamp: '2018-02-20:15:31.000Z',
    body: 'Hello Ana',
  },
  {
    subject: 'URGENT: Processed payments',
    from: {
      name: 'Bea Bright',
      email: 'Bea.bright@email.com',
    },
    id: '5bdebcf9-7911-4757-befd-d2bc86f0ffdb',
    timestamp: '2018-02-20:15:31.000Z',
    body: 'Hello Ana',
  },
  {
    subject: 'Cool pic',
    from: {
      name: 'Danielle Day',
      photoUrl: 'https://randomuser.me/api/portraits/women/67.jpg',
      email: '12eada382@298daef9390.co',
    },
    id: '261ef797-4b88-4c60-94db-7e4ab31682e8',
    timestamp: '2018-02-20:15:31.000Z',
    body: 'Check this out! Maybe we could use it for a flyer ;)',
  },
  {
    subject: 'Refund participant',
    from: {
      name: 'Geoff Dave',
      email: 'geoffrey.david@company.com',
    },
    id: '54476574-cc91-4e9a-b366-424b0aaed34d',
    timestamp: '2018-02-20:15:31.000Z',
    body: 'Hello Ana',
  },
  {
    subject: 'Suspicious Activity',
    from: {
      name: 'MoneyTransfer',
      email: 'moneytransfersucpsicions@email.com',
    },
    id: 'ec705f8a-9492-4ab4-8768-f979bbdba760',
    timestamp: '2018-02-20:15:31.000Z',
    body: 'Hello Ana',
  },
];

export function getEmail(id) {
  return EMAILS.find(email => email.id === id);
}

export function getAllEmails() {
  return EMAILS;
}
