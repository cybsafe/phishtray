const FILES = [
  {
    id: '001',
    fileName: 'World Cup',
    description: `It's coming home`,
    dateCreated: '26/12/2018',
    fileUrl: `https://images.unsplash.com/photo-1518091043644-c1d4457512c6?ixlib=rb-0.3.5&s=32e020e5b98c97af64924afa1eb76c35&auto=format&fit=crop&w=800&q=60`,
  },
  {
    id: '002',
    fileName: 'Machu Picchu',
    description: 'Trip to Peru',
    dateCreated: '19/04/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  },
  {
    id: '003',
    fileName: 'Burgers',
    description: `It's BBQ weather`,
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522244451342-a41bf8a13d73?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=ecb72e30ff69d3942629286b785b7f6e&auto=format&fit=crop&w=1500&q=80`,
  },
  {
    id: '004',
    fileName: 'Beer on the beach',
    description: 'This is the life!',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1473429174434-a8a8d5e0dc2e?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=703b6db7761c9073368fd199592e6c6c&auto=format&fit=crop&w=800&q=60`,
  },
  {
    id: '005',
    fileName: 'Working hard',
    description: 'Or hardly working',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1517852058149-07c7a2e65cc6?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=0f790f4ced3c54118391c71f534597ed&auto=format&fit=crop&w=1350&q=80`,
  },
  {
    id: '006',
    fileName: 'Cake',
    description: 'The cake is a lie',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1518047601542-79f18c655718?ixlib=rb-0.3.5&s=56d4b169a734d5e7ee6ef3c7286fb29c&auto=format&fit=crop&w=800&q=60`,
  },
  {
    id: '007',
    fileName: 'Xbox',
    description: 'Time for some downtime',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1512686096451-a15c19314d59?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=52356ca48e4027e1f34c5c58255696f3&auto=format&fit=crop&w=1500&q=80`,
  },
];

export function getAllFiles() {
  return FILES;
}
