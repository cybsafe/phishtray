import React from 'react';
import styled from 'react-emotion';

const Container = styled('div')`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
`;

const ContentWrapper = styled('div')`
  max-width: 648px;
`;

const Title = styled('h1')`
  margin-top: 80px;
  margin-bottom: 60px;
  color: #262939;
  font-size: 48px;
`;
const P = styled('p')`
  margin-bottom: 26px;
  color: #909196;
  font-size: 18px;
`;

const BulletListContainer = styled('div')`
  display: flex;
  justify-content: center;
  align-items: center;
`;
const BulletList = styled('ul')`
  color: #909196;
  font-size: 18px;
  line-height: 26px;
  text-align: left;
  list-style-type: initial;
  align-self: center;
`;

const Warning = () => {
  return (
    <Container>
      <ContentWrapper>
        <Title>Warning - Phishing Simulation</Title>
        <P>
          <strong>What just happened?</strong>
          <br /> The email you just opened and followed a link from was in fact
          a simulated phishing attack.
        </P>
        <P>
          Don’t worry, no details you entered were recorded. However, if this
          was a real attack, you may have just handed sensitive information to a
          criminal which could have allowed them to access your personal
          information.
        </P>
        <P>
          Remember, whenever you receive an email you
          <strong> weren't expecting</strong>, ask yourself three questions:
        </P>
        <BulletListContainer>
          <BulletList>
            <li>
              Does it ask me to<strong> break policy</strong>?
            </li>
            <li>
              Does it convey an<strong> undue sense of urgency</strong>?
            </li>
            <li>
              Does it include a
              <strong> link or attachment I don't recognize</strong>?
            </li>
          </BulletList>
        </BulletListContainer>
      </ContentWrapper>
    </Container>
  );
};

export default Warning;
