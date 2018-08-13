from ...models import Exercise, ExerciseEmail, ExerciseEmailsThrough \
                            ,ExerciseAttachment, ExerciseEmailReply \
                            ,EXERCISE_EMAIL_PHISH

def create_exercise_3_emails():
    '''More complicated test case - exercise containing 3 emails,
       attacment and replies. Example taken from your site:
       http://phishtray.cybsafedev.com:8000/exercise/detail/1/
    '''
    #Exercise
    exercise = Exercise.objects.create(
        id=1,
        title='Exercise A. Changing the world.',
        description='This is the administrator description of the exercise',
        introduction='<h1>Important Life Changing Exercise</h1>\r\n<br>\r\n<p>\r\nThis is such an important exercise to understand just how you will go about changing the world.\r\n</p>\r\n<img width=\"80%\" src=\"https://media1.popsugar-assets.com/files/thumbor/_XIv2PMlWMie6FmqWMBh7pr-XHk/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2017/09/19/992/n/36735815/c5a39fb959c04d658f6b73.48321050_edit_img_cover_file_37438685_1477814400/i/39-Inspirational-Quotes-Change-Your-Life.jpg\">',
        afterword = 'This is the completing text for an experiment.',
        length_minutes=5
    )

    #Replies
    reply_1 = ExerciseEmailReply.objects.create(
            id=1,
            reply_type=0,
            message='No thanks this looks like spam?'

        )

    reply_2 = ExerciseEmailReply.objects.create(
            id=2,
            reply_type=1,
            message='Hey look at this rubbish!'

        )

    #Attachments
    attachment_1 = ExerciseAttachment.objects.create(
        id = 1,
        filename ='Lies.PDF'
    )

    #Emails
    email_1 = ExerciseEmail.objects.create(
        id=1,
        subject='Your account has been locked',
        from_address='serious@fraud.com',
        from_name='Secure Banking',
        to_address='you@test.com',
        to_name='James',
        phish_type=0,
        content='Some fraud has occured...',
    )

    email_2 = ExerciseEmail.objects.create(
        id=2,
        subject='Hey take a look at this',
        from_address='yourfriend@gmail.com',
        from_name='Friend',
        to_address='you@gmail.com',
        to_name='Name',
        phish_type=1,
        content="Hey how's it going? Seriously it's been a very long time!",
    )
    email_2.replies.add(reply_1, reply_2)
    email_2.attachments.add(attachment_1)
    
       
    email_3 = ExerciseEmail.objects.create(
        id=3,
        subject='How are you?',
        from_address='serious@fraud.com',
        from_name='Friend',
        to_address='you@test.com',
        to_name='Name',
        phish_type=0,
        content="There's a deal I think you'd be really interested in!",
    )
    email_3.replies.add(reply_1, reply_2)
    

    #Linking exercis and emails
    #I assume, by default, reveal_time = None. It can be changed depend on requrements
    exercise_email_1 = ExerciseEmailsThrough.objects.create(exercise = exercise,
                                            exerciseemail = email_1)

    exercise_email_2 = ExerciseEmailsThrough.objects.create(exercise = exercise,
                                            exerciseemail = email_2)
    
    exercise_email_3 = ExerciseEmailsThrough.objects.create(exercise = exercise,
                                            exerciseemail = email_3)

def create_exercise_20_emails():

    #Exercise
    exercise = Exercise.objects.create(
        id = 1,
        title='Exercise A. Changing the world.',
        description='This is the administrator description of the exercise',
        introduction='test',
        afterword = 'This is the completing text for an experiment.',
        length_minutes=10
    )

    #Emails and add to exercise
    for i in range(20):
        email = ExerciseEmail.objects.create(phish_type=EXERCISE_EMAIL_PHISH,
                                            subject = 'test email {}'.format(i))
        exercise_email = ExerciseEmailsThrough.objects.create(exercise = exercise
                                            ,exerciseemail = email)

    exercise.generate_reveal_time()
    return exercise

def create_two_exercises_20_emails():

    #Exercise
    exercise_1 = Exercise.objects.create(
        id = 1,
        title='Exercise A. Changing the world.',
        description='This is the administrator description of the exercise',
        introduction='test',
        afterword = 'This is the completing text for an experiment.',
        length_minutes=10
    )

    exercise_2 = Exercise.objects.create(
        id = 2,
        title='Exercise B. Changing the world.',
        description='This is the administrator description of the exercise',
        introduction='test',
        afterword = 'This is the completing text for an experiment.',
        length_minutes=10
    )

    #Emails and add to exercise
    for i in range(20):
        email = ExerciseEmail.objects.create(phish_type=EXERCISE_EMAIL_PHISH,
                                            subject = 'test email {}'.format(i))
        exercise_1_email = ExerciseEmailsThrough.objects.create(exercise = exercise_1
                                            ,exerciseemail = email)
        exercise_2_email = ExerciseEmailsThrough.objects.create(exercise = exercise_2
                                            ,exerciseemail = email)

    exercise_1.generate_reveal_time()
    exercise_2.generate_reveal_time()
    return (exercise_1,exercise_2)