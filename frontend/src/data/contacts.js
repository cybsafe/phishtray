const CONTACTS = [
  {
    name: 'Stephanie Cross',
    id: '1',
    image: 'https://s3-eu-west-1.amazonaws.com/project-shower/Card1.png',
  },
  {
    name: 'Jason Field',
    id: '2',
    image: 'https://s3-eu-west-1.amazonaws.com/project-shower/Card2.png',
  },
  {
    name: 'Organisational Chart',
    id: '3',
    image:
      'https://s3-eu-west-1.amazonaws.com/project-shower/Org+chart+card.png',
  },
];

export function getContact(id) {
  return CONTACTS.find(contact => contact.id === id);
}

export function getAllContacts() {
  return CONTACTS;
}
