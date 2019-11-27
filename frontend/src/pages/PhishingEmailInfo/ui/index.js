import styled from 'react-emotion';
import { Button } from 'carbon-components-react';

export const Title = styled('h3')`
  margin: 30px 0 20px;
  font-weight: 600;
  font-size: 48px;
  color: #262939;
`;

export const Container = styled('section')`
  max-width: 960px;
  padding: 0 15px;
  margin: 0 auto 30px;
  width: 100%;
`;

export const EmailItemField = styled('ul')`
  background-color: rgba(13, 121, 205, 0.05);
  box-shadow: 0 0 2px #0d79cd;
  border: 1px solid #0d79cd;
  margin: 0 0 20px 0;
  padding: 18px 25px;
  list-style: none;
`;

export const EmailItemContent = styled('li')`
  font-size: 22px;
  color: #909196;
  line-height: 1.5;
  font-weight: ${({ fault }) => (fault === 'fault' ? '700' : '300')};

  &:not(:last-child) {
    margin-bottom: 15px;
  }
`;

export const Emphasis = styled('span')`
  font-weight: bold;
  display: inline-block;
  margin-right: 10px;
`;

export const ButtonsContainer = styled('div')`
  justify-content: flex-end;
  display: flex;
`;

export const AppButton = styled(Button)`
  transition: none;

  &:not(:first-child) {
    margin-left: 15px;
  }
`;

const BehaviorField = styled('span')`
  display: block;
  font-size: 24px;

  > svg {
    margin-right: 20px;
  }
`;

export const BehaviorFieldSuccess = styled(BehaviorField)`
  color: #2cb899;
`;

export const BehaviorFieldNegative = styled(BehaviorField)`
  color: #ff0000;
`;

export const SeeDetails = styled(Button)`
  margin-bottom: 15px;
  appearance: none;
  font-size: 16px;
  display: block;
  padding: 12px;
`;
