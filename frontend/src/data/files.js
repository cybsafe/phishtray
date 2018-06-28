const FILES = [
  {
    id: '001',
    fileName: 'File 1',
    description: 'this is a description',
    dateCreated: '26/12/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '002',
    fileName: 'File 2',
    description: 'this is another description',
    dateCreated: '19/04/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '003',
    fileName: 'File 3',
    description: 'I like big butts and I cannot lie',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '004',
    fileName: 'File 4',
    description: 'On a field trip',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '005',
    fileName: 'File 5',
    description: 'Lots of cake',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '006',
    fileName: 'File 6',
    description: 'Love a burrito',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  }, {
    id: '007',
    fileName: 'File 7',
    description: 'mmmmm kfc',
    dateCreated: '19/05/2018',
    fileUrl: `https://images.unsplash.com/photo-1522451056252-3fa650a3b8bf?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=4f2a9188d152c2c646dd9f5c2c614102&auto=format&fit=crop&w=1350&q=80`,
  },
];

export function getAllFiles() {
  return FILES;
}
