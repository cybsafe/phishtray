// @flow
import React from 'react';
import styled, { css } from 'react-emotion';
import { type Match } from 'react-router-dom';
import { getContact } from '../../../data/contacts';

type Props = {
  match: Match,
};

const BodyContainer = styled('div')({
  maxWidth: 880,
  margin: '0 auto',
  padding: '0 40px',
});

const Spacer = styled('div')({ height: 40 });

const ContactImage = ({ url }) => (
  <img src={url} width="100%" heigh="100%" alt="information" />
);

const Contact = (props: Props) => {
  const { match } = props;
  const {
    params: { id },
  } = match;
  const contact = getContact(id);

  return (
    <BodyContainer>
      <h3
        className={css({
          marginTop: 40,
          fontSize: 40,
          color: '#333',
          letterSpacing: '1.2px',
        })}
      >
        {contact.name}
      </h3>

      <Spacer />
      <ContactImage url={contact.image} />
    </BodyContainer>
  );
};

export default Contact;
