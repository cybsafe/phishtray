# Action types are listed in frontend/src/config/actionTypes.js
# TODO: move actiontypes to a config file that
#       can be parsed/imported by both python and js

NEGATIVE_ACTIONS = [
    "email_attachment_download",
    "email_forwarded",
    "email_link_clicked",
    "email_quick_reply",
    "email_replied",
]

POSITIVE_ACTIONS = ["email_reported", "email_deleted"]


class ParticipantBehaviour:
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
