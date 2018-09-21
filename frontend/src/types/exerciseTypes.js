// @flow
export type FormQuestion = {
  id: string,
  question: string,
  questionType: number,
  required: true | false,
};

export type ExerciseEmailAccount = {
  email: string,
  name: string,
  photoUrl: string | null,
  role: string | null,
};

export type ExerciseEmailAttachment = {
  id: string,
  filename: string,
};

export type ExerciseEmailReply = {
  id: string,
  replyType: number,
  message: string,
};

export type ExerciseEmail = {
  id: string,
  subject: string,
  phishType: number,
  fromAccount: ExerciseEmailAccount,
  toAccount: ExerciseEmailAccount,
  body: string,
  attachments: ExerciseEmailAttachment[],
  replies: ExerciseEmailReply[],
};

export type ExerciseThread = {
  id: string,
  subject: string,
  fromAccount: ExerciseEmailAccount,
  toAccount: ExerciseEmailAccount,
  body: string,
  attachments: ExerciseEmailAttachment[] | [],
  replies: ExerciseEmailReply[] | [],
  emails: ExerciseEmail[] | [],
  isRead: boolean,
};

export type EmailRevealTime = {
  emailId: string,
  revealTime: number,
};
