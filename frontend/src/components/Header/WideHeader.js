// @flow

import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import styled from 'react-emotion';

const Content = styled('div')({
  width: '100%',
  minHeight: '200px',
  backgroundColor: '#0a79cd',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

const ContentContainer = styled('div')({
  display: 'flex',
  width: '60%',
  maxWidth: '1000px',
  marginTop: '70px',
  marginBottom: '70px',
});

const InnerWrapper = styled('div')({
  maxWidth: '1000px',
  justifyContent: 'flex',
  flexDirection: 'column',
  position: 'relative',
  right: '5%',
});

const Icon = styled(FontAwesomeIcon)({
  position: 'relative',
  right: '10%',
});

const Title = styled('h1')({
  color: '#fff',
  fontSize: '3rem',
  fontWeight: 500,
});

const Subtitle = styled('p')({
  color: '#fff',
  fontSize: '1.5rem',
  fontWeight: 300,
});

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
