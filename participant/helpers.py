from .models import ParticipantAction, STARTED_EXPERIMENT, COMPLETED_EXPERIMENT, \
    OPENED_EMAIL, OPENED_UNSAFE_EMAIL_LINK, DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT


class LogParticipantAction:

    def __init__(self, participant, experiment):
        self.participant = participant
        self.experiment = experiment
        self.email = None

    def experiment_started(self):
        action = ParticipantAction.create(
            type=STARTED_EXPERIMENT,
            participant=self.participant,
            experiment=self.experiment,
            email=self.email
        )
        action.save()

    def experiment_ended(self):
        action = ParticipantAction.create(
            type=COMPLETED_EXPERIMENT,
            participant=self.participant,
            experiment=self.experiment,
            email=self.email
        )
        action.save()

    def email_opened(self, email):
        self.email = email
        action = ParticipantAction.create(
            type=OPENED_EMAIL,
            participant=self.participant,
            experiment=self.experiment,
            email=self.email
        )
        action.save()

    def email_link_opened(self):
        action = ParticipantAction.create(
            type=OPENED_UNSAFE_EMAIL_LINK,
            participant=self.participant,
            experiment=self.experiment,
            email=self.email
        )
        action.save()

    def email_attachment_downloaded(self):
        action = ParticipantAction.create(
            type=DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT,
            participant=self.participant,
            experiment=self.experiment,
            email=self.email
        )
        action.save()
