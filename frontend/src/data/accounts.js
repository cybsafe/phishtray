const ACCOUNTS = [
  {
    name: 'PayPal',
    id: 'fa59b235-184f-40ba-aae7-daaf48689d22',
    data:[{
      key: 'Username',
      value: 'biggeoff@gmail.com',
      },
      {
      key: 'Password',
      value: 'someSeriouslySecure3Password',
      },
    ],
  },
 {
    name: 'PayDayve',
    id: 'fa59b235-184f-40ba-aae7-dtf48689d22',
    data:[{
      key: 'Username',
      value: 'biggeoff@gmail.com',
      },
      {
      key: 'Password',
      value: 'someSeriouslySecure3Password',
      },
    ],
  },
 {
    name: 'HBSC',
    id: 'fa59b235-184f-40ba-aae7-d3tf48689d22',
    data:[
    {
      key: 'PIN',
      value: '1234',
      },
      {
      key: 'Username',
      value: 'bg5678',
      },
      {
      key: 'Password',
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
