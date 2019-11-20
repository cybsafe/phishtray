export const negativeMessages = actionType => {
  switch (actionType) {
    case 'email_attachment_download':
      return 'You should not have downloaded this file!';
    case 'email_forwarded':
      return 'You should not forward this email!';
    case 'email_link_clicked':
      return 'You should not have clicked on this link!';
    case 'email_quick_reply':
    case 'email_replied':
      return 'You should not have answered this email!';
    default:
      return 'This was a high risk thing to do!';
  }
};

export const positiveMessages = actionType => {
  switch (actionType) {
    case 'email_reported':
      return 'You reported this email!';
    case 'email_deleted':
      return 'You deleted this email!';
    default:
      return 'This was a low risk thing to do!';
  }
};

export const sanitizeActions = actionType => {
  switch (actionType) {
    case 'email_reported':
      return 'Email reported';
    case 'email_opened':
      return 'Email opened';
    case 'email_deleted':
      return 'Email deleted';
    case 'email_attachment_download':
      return 'Download email attachment';
    case 'email_forwarded':
      return 'Email forwarded';
    case 'email_link_clicked':
      return 'Clicked link';
    case 'email_quick_reply':
      return 'Quickly email replied';
    case 'email_replied':
      return 'Email replied';
    default:
      return 'Action not founded';
  }
};
