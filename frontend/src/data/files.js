const FILES = [
  {
    id: '001',
    fileName: 'Supplier check',
    description: `Supplier check`,
    dateCreated: '2018-12-26',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/supplier+check.jpg`,
  },
  {
    id: '002',
    fileName: 'Computer unit',
    description: 'Computer unit',
    dateCreated: '2018-04-19',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/computer+unit.jpg`,
  },
  {
    id: '003',
    fileName: 'Supplier notes',
    description: `Supplier notes`,
    dateCreated: '2018-05-19',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/supplier+notes.jpg`,
  },
  {
    id: '004',
    fileName: 'Course notes',
    description: 'Course notes',
    dateCreated: '2018-05-19',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/course+notes.jpg`,
  },
  {
    id: '005',
    fileName: 'Invoice',
    description: 'Invoices',
    dateCreated: '2018-06-19',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/invoice.jpg`,
  },
  {
    id: '006',
    fileName: 'Your calendar screen',
    description: 'Your calendar screen',
    dateCreated: '2018-06-25',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/your+calendar.png`,
  },
  {
    id: '007',
    fileName: 'Stephanie`s calendar',
    description: 'Stephanie`s calendar',
    dateCreated: '2018-07-01',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/stephanies+calendar.png`,
  },
  {
    id: '008',
    fileName: 'Jason`s calendar',
    description: 'Jason`s calendar',
    dateCreated: '2018-07-01',
    fileUrl: `https://s3-eu-west-1.amazonaws.com/project-shower/jasons+calendar.png`,
  },
];

export function getAllFiles() {
  return FILES;
}
