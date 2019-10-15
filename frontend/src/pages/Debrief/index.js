//@flow
import React, { useEffect, Fragment } from 'react';
import styled, { injectGlobal } from 'react-emotion';
import { connect } from 'react-redux';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import image from './assets/image_emails.png';
import { Button as CarbonButton } from 'carbon-components-react';

const RuiHeader = styled('header')`
  background-color: #0a79cd;
  justify-content: center;
  align-items: center;
  height: 200px;
  display: flex;

  h2 {
    font-size: 48px;
    color: white;
    margin: 0;
  }
`;

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

injectGlobal`
  #root {
    background-color: white;
  }
`;

type Props = {
  match: Object,
  params: Object,
  getDebrief: (*) => void,
  phishingEmails: Array<*>,
};

function Debrief({
  match: {
    params: { participantUuid },
  },
  getDebrief,
  phishingEmails,
}: Props) {
  useEffect(() => {
    getDebrief(participantUuid);
  }, [participantUuid]);

  if (phishingEmails.length <= 0) {
    return false;
  }

  return (
    <Fragment>
      <RuiHeader>
        <h2>Rui's Header here</h2>
      </RuiHeader>
      <Container>
        <ResultMessage>
          You were given {phishingEmails.length} phishing emails!
        </ResultMessage>
        <Image src={image} />
        <Button kind="primary" onClick={() => console.log('Showing Details')}>
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
