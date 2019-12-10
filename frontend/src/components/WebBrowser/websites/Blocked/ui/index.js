import styled from 'react-emotion';
import { TextInput, Button } from 'carbon-components-react';

export const Wrapper = styled('section')`
  min-height: calc(100vh - 120px);
  background-color: #9c3c34;
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
  color: white;
`;

export const Text = styled('p')`
  margin-bottom: 80px;
  text-align: center;
  font-size: 18px;
  color: #ffffff;
`;

export const Form = styled('form')`
  width: 100%;

  .bx--form-item {
    width: 100%;
  }

  .bx--form-requirement {
    background-color: #ffffff;
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
  }
`;

export const Input = styled(TextInput)`
  border-radius: 6px !important;
  background-color: transparent;
  border: 1px solid #ffffff;
  border-color: #ffffff;
  color: #ffffff;
  height: 60px;
  width: 100%;
  margin-bottom: 8px;
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
