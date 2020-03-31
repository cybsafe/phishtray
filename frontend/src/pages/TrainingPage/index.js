// @flow
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import styled from 'react-emotion';
import { Button as CarbonButton } from 'carbon-components-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';
import WideHeader from '../../components/Header/WideHeader';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import { logAction } from '../../utils';

import image from './assets/image13.png';
import withErrorBoundary from "../../errors/ErrorBoundary";

const Container = styled('div')`
  display: flex;
  align-items: center;
  min-height: 100%;
  background-color: #fff;
  flex-direction: column;
`;

const ContentContainer = styled('div')`
  max-width: 1000px;
  width: 60%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: flex-end;
  margin-top: 3rem;
  margin-bottom: 3rem;
  height: calc(100vh - 200px - 6rem);
  min-height: 450px;
`;

const Image = styled('img')`
  margin: 0 auto;
  display: block;
  height: auto;
`;

const Message = styled('h3')`
  font-size: 2.8vw;
  text-align: center;
  color: #262939;
`;

const Button = styled(CarbonButton)`
  margin-right: 3rem;
`;

const Icon = styled(FontAwesomeIcon)`
  margin-left: 10px;
`;

type Props = {
  trainingLink: string,
  match: {
    params: {
      participantUuid: string,
    },
  },
};

const TrainingPage = (props: Props) => {
  const { participantUuid } = props.match.params;
  const { trainingLink } = props;
  useEffect(() => {
    getDebrief(participantUuid);
  }, [participantUuid]);

  return (
    <Container>
      <WideHeader title="Thanks for taking the exercise." />
      <ContentContainer>
        <Message>
          Here is a <em>free</em> resource to learn more about phishing
        </Message>
        <Image src={image} />
        <Button
          kind="primary"
          onClick={() => {
            logAction({
              actionType: 'training_link_clicked',
              participantId: participantUuid,
              startTime: Date.now(),
            });
            window.open(
              trainingLink !== ''
                ? trainingLink
                : 'https://app.cybsafe.com/phishtray?login=false'
            );
          }}
        >
          Take me to free resource
          <Icon icon={faExternalLinkAlt} />
        </Button>
      </ContentContainer>
    </Container>
  );
};

export default connect(
  state => ({
    trainingLink: state.debrief.trainingLink,
  }),
  { getDebrief }
)(withErrorBoundary(withRouter(TrainingPage)));
