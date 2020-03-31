//@flow
import React, { useEffect, Fragment } from 'react';
import styled from 'react-emotion';
import { useDispatch, useSelector } from 'react-redux';
import { Button as CarbonButton } from 'carbon-components-react';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import WideHeader from '../../components/Header/WideHeader';
import withErrorBoundary from '../../errors/ErrorBoundary';

import image from './assets/image_emails.png';

const BGWrapper = styled('div')`
  min-height: calc(100vh - 236px);
  background-color: white;
  padding: 216px 0 100px;
`;

const Container = styled('section')`
  max-width: 960px;
  padding: 0 15px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
`;

const ResultMessage = styled('h3')`
  margin-bottom: 44px;
  text-align: center;
  font-size: 48px;
  color: #262939;
`;

const Image = styled('img')`
  margin: 0 auto;
  display: block;
  height: auto;
`;

const Button = styled(CarbonButton)`
  align-self: flex-end;
`;

const NotFound = styled('h2')`
  transform: translate(-50%, -50%);
  position: absolute;
  left: 50%;
  top: 50%;
  margin: 0;
`;

type Props = {
  match: Object,
  params: Object,
  history: Object,
};

const NotFoundPage = () => <NotFound>participantUuid not found.</NotFound>;

function Debrief({
  match: {
    params: { participantUuid },
  },
  history,
}: Props) {
  const phishingEmails = useSelector(state => state.debrief.phishingEmails);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getDebrief(participantUuid));
  }, [participantUuid, dispatch]);

  if (phishingEmails === undefined) {
    return NotFoundPage();
  }

  if (phishingEmails.length <= 0) {
    return false;
  }

  return (
    <Fragment>
      <WideHeader
        title="Thanks for taking the exercise"
        subtitle="Find out more"
      />
      <BGWrapper>
        <Container>
          <ResultMessage>
            You were given {phishingEmails.length} phishing{' '}
            {phishingEmails.length > 1 ? 'emails' : 'email'}!
          </ResultMessage>
          <Image src={image} />
          <Button
            kind="primary"
            onClick={() =>
              history.push(`/phishing-email-info/${participantUuid}`)
            }
          >
            Show Me Details
          </Button>
        </Container>
      </BGWrapper>
    </Fragment>
  );
}

export default withErrorBoundary(Debrief);
