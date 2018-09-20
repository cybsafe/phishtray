const THREADS = [
  {
    id: '0',
    subject: 'Welcome on board!',
    fromAccount: 'Arther Ardent',
    revealTime: 5, // reveal after 5 seconds
    emails: [
      {
        subject: 'Welcome on board!',
        fromAccount: {
          name: 'Arther Ardent',
          photoUrl: 'https://randomuser.me/api/portraits/men/32.jpg',
          email: 'a.ardent@email.com',
          role: 'MD',
        },
        id: 'fa59b235-184f-40ba-aae7-daaf48689d22',

        body: `Hello,\n\nThank you for helping out with the conference organisation. Great to have you on board!\n\nWe are about to make the pay run and need your bank details...\n\nThanks, Arther`,
      },
    ],
  },
  {
    id: '1',
    subject: 'Caution with emails',
    fromAccount: 'Peter Pollard',
    revealTime: 0,
    emails: [
      {
        subject: 'Caution with emails',
        fromAccount: {
          name: 'Peter Pollard',
          photoUrl: 'https://randomuser.me/api/portraits/men/79.jpg',
          email: 'peter.pollard1@email.com',
        },
        id: '6e42899c-b868-4fa6-af3c-5a6bdf2ef346f',

        body:
          'Hey team,\n\nDid you all receive my warning about spam emails trying to obtain your bank details?',
      },
      {
        subject: 'Caution with emails',
        fromAccount: {
          name: 'Me',
          photoUrl: 'https://randomuser.me/api/portraits/women/83.jpg',
        },
        id: '6e42899c-3868-4fa6-af3c-5a6bdf67ef66f',

        body:
          "No I didn't see the warning!,\n\nI had a load of banking emails this morning! Is it too late?",
      },
      {
        subject: 'Caution with emails',
        fromAccount: {
          name: 'Peter Pollard',
          photoUrl: 'https://randomuser.me/api/portraits/men/79.jpg',
          email: 'peter.pollard1@email.com',
        },
        id: '6e42899c-b868-4fa6-af3c-5a63451f2ef66f',

        body: 'Oh dear,\n\nSpeak to your bank immediately!',
        replies: [
          {
            id: 5,
            type: 'reply',
            message: "Nah, it's fine",
          },
          {
            id: 6,
            type: 'reply',
            message: "Ok I'll do it right away!",
          },
        ],
      },
    ],
  },
  {
    id: '2',
    subject: 'URGENT: Processed payments',
    fromAccount: 'Bea Bright',
    revealTime: 0,
    emails: [
      {
        subject: 'URGENT: Processed payments',
        fromAccount: {
          photoUrl: 'https://randomuser.me/api/portraits/women/12.jpg',
          name: 'Bea Bright',
          email: 'Bea.bright@email.com',
        },
        id: '5bdebcf9-7911-4757-befd-d2bc86f0ffdb',

        body: 'Hello, can you take a look at this please?',
        attachments: [
          {
            id: 124,
            filename: 'Trustme.exe',
          },
        ],
        replies: [
          {
            id: 5,
            type: 'reply',
            message: "I'm really sorry that can't be done",
          },
          {
            id: 6,
            type: 'forward',
            message: "Hey could you check this - I'm not sure about it",
          },
        ],
      },
    ],
  },
  {
    id: '3',
    subject: 'Cool pic',
    fromAccount: 'Danielle Day',
    revealTime: 0,
    emails: [
      {
        subject: 'Cool pic',
        fromAccount: {
          name: 'Danielle Day',
          photoUrl: 'https://randomuser.me/api/portraits/women/67.jpg',
          email: '12eada382@298daef9390.co',
        },
        id: '261ef797-4b88-4c60-94db-7e4ab31682e8',

        body: 'Check this out! Maybe we could use it for a flyer ;)',
        attachments: [
          {
            id: 124,
            filename: 'innocent_jpeg.exe',
          },
        ],
      },
    ],
  },
  {
    id: '4',
    subject: 'Refund Request',
    fromAccount: '[HBSC] Geoff Dave',
    revealTime: 0,
    emails: [
      {
        subject: 'Refund Request',
        fromAccount: {
          name: 'Geoff Dave',
          email: 'geoffrey@hbsc.mailsender.awe2.com',
        },
        id: '54476574-cc91-4e9a-b366-424b0aaed34d',

        body:
          '# Good afternoon,\n\nWe recently received a request to process a refund request on your account. Before we deposit the money, HBSC require confirmation from you.\n\n \n\n [Please click here to release your money](/#)',
      },
    ],
  },
  {
    id: '5',
    subject: 'Suspicious Activity',
    fromAccount: 'PayFriend',
    revealTime: 0,
    emails: [
      {
        subject: 'Suspicious Activity',
        fromAccount: {
          name: 'PayFriend',
          email: 'oz_1991@hotmail.com',
        },
        id: 'ec705f8a-9492-4ab4-8768-f979bbdba760',

        body:
          'Hello there!, we have evidence of suspicious activity on your account, please see the records below',
        attachments: [
          {
            id: 124,
            filename: 'innocent_jpeg.exe',
          },
        ],
      },
    ],
  },
];

export function getThread(id) {
  return THREADS.find(thread => thread.id === id);
}

export function getEmail(id) {
  return THREADS.find(email => email.id === id);
}

export function getAllEmails() {
  return THREADS;
}
