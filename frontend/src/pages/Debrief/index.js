//@flow
import React, { useEffect, Fragment } from 'react';
import styled, { injectGlobal } from 'react-emotion';
import { connect } from 'react-redux';
import { Button as CarbonButton } from 'carbon-components-react';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import WideHeader from '../../components/Header/WideHeader';

import image from './assets/image_emails.png';

const Container = styled('section')`
  max-width: 960px;
  padding: 0 15px;
  margin: 0 auto;
  width: 100%;
`;

const ResultMessage = styled('h3')`
  margin: 8.583vw 0 4.472vw;
  font-size: 2.8vw;
  text-align: center;
  color: #262939;
`;

const Image = styled('img')`
  margin: 0 auto;
  display: block;
  height: auto;
`;

const Button = styled(CarbonButton)`
  float: right;
`;

const NotFound = styled('h2')`
  transform: translate(-50%, -50%);
  position: absolute;
  left: 50%;
  top: 50%;
  margin: 0;
`;

injectGlobal`
  #root {
    background-color: white;
  }
`;

type Props = {
  match: Object,
  params: Object,
  history: Object,
  getDebrief: (*) => void,
  phishingEmails: Array<*>,
};

const NotFoundPage = () => <NotFound>participantUuid not found.</NotFound>;

function Debrief({
  match: {
    params: { participantUuid },
  },
  history,
  getDebrief,
  phishingEmails,
}: Props) {
  useEffect(() => {
    getDebrief(participantUuid);
  }, [participantUuid, getDebrief]);

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
    </Fragment>
  );
}

export default connect(
  state => ({
    phishingEmails: state.debrief.phishingEmails,
  }),
  { getDebrief }
)(Debrief);
