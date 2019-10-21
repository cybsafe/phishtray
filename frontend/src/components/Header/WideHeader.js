// @flow

import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import styled from 'react-emotion';

const Content = styled('div')`
  width: 100%;
  min-height: 200px;
  background-color: #0a79cd;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const ContentContainer = styled('div')`
  display: flex;
  width: 60%;
  max-width: 1000px;
  margin-top: 70px;
  margin-bottom: 70px;
`;

const InnerWrapper = styled('div')`
  max-width: 1000px;
  justify-content: flex;
  flex-direction: column;
  position: relative;
  right: 5%;
`;

const Icon = styled(FontAwesomeIcon)`
  position: relative;
  right: 10%;
`;

const Title = styled('h1')`
  color: #fff;
  font-size: 3rem;
  font-weight: 500;
`;

const Subtitle = styled('p')`
  color: #fff;
  font-size: 1.5rem;
  font-weight: 300;
`;

function WideHeader({ title, subtitle }: { title: string, subtitle?: string }) {
  return (
    <Content>
      <ContentContainer>
        <Icon icon={faThumbsUp} color="#fff" size="3x" />
        <InnerWrapper>
          <Title>{title}</Title>
          {subtitle && <Subtitle>{subtitle}</Subtitle>}
        </InnerWrapper>
      </ContentContainer>
    </Content>
  );
}

export default WideHeader;
