const ACCOUNTS = [
  {
    name: 'My Payment',
    id: 'fa59b235-184f-40ba-aae7-daaf48689d22',
    data: [
      {
        id: '2',
        label: 'Email Address',
        value: 'biggeoff@gmail.com',
      },
    ],
  },
  {
    name: 'Bluestar',
    id: 'fa59b235-284f-40ba-aae7-dtf48689d22',
    data: [
      {
        id: '3',
        label: 'Password',
        value: 'someSeriouslySecure3Password',
      },
    ],
  },
  {
    name: 'HBSC',
    id: 'fa59b235-384f-40ba-aae7-d3tf48689d22',
    data: [
      {
        id: '4',
        label: 'PIN',
        value: '1234',
      },
      {
        id: '5',
        label: 'Username',
        value: 'bg5678',
      },
      {
        id: '6',
        label: 'Password',
        value: 'someSeriouslySecure3Password',
      },
    ],
  },
];

export function getAccount(id) {
  return ACCOUNTS.find(account => account.id === id);
}

export function getAllAccounts() {
  return ACCOUNTS;
}
