import styled from 'react-emotion';
import { TextInput, Button } from 'carbon-components-react';

export const Wrapper = styled('section')`
  min-height: calc(100vh - 120px);
  background-color: #ffffff;
  overflow-y: scroll;
  position: relative;
  padding: 60px 0;
`;

export const Container = styled('div')`
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
  text-align: center;
`;

export const Title = styled('h1')`
  margin: 30px 0 60px;
  text-align: center;
  font-size: 48px;
  color: #999999;
`;

export const MarkDownContainer = styled('p')`
  margin-bottom: 2rem;
  font-size: 1rem;
  p {
    text-align: center;
    font-size: 18px;
    color: #999999;
    margin-bottom: 1rem;
  }
`;

export const Text = styled('p')`
  margin-bottom: 80px;
  text-align: center;
  font-size: 18px;
  color: #999999;
`;

export const Form = styled('form')`
  width: 100%;

  .bx--form-item {
    width: 100%;
  }
`;

export const Input = styled(TextInput)`
  border-radius: 6px !important;
  background-color: transparent;
  border: 1px solid #999999;
  border-color: #999999;
  color: #666666;
  height: 60px;
  width: 100%;
  margin-bottom: 8px;
  box-shadow: none;
`;

export const Clear = styled('div')`
  zoom: 1;

  &:after {
    content: '';
    display: table;
  }

  &:after {
    content: '';
    display: table;
    clear: both;
  }
`;

export const SubmitButton = styled(Button)`
  border-radius: 6px;
  min-width: 150px;
  height: 50px;
  float: right;
  margin-top: 20px;
`;
