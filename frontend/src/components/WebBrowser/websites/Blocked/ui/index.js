import styled from 'react-emotion';
import { TextInput, Button } from 'carbon-components-react';

export const Wrapper = styled('section')`
  background-color: #9c3c34;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  display: flex;
`;

export const Container = styled('div')`
  flex-direction: column;
  margin-bottom: 100px;
  align-items: center;
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  width: 100%;
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
  flex-direction: column;
  display: flex;
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

export const SubmitButton = styled(Button)`
  border-radius: 6px;
  min-width: 150px;
  height: 50px;
  align-self: flex-end;
  margin-top: 20px;
`;
