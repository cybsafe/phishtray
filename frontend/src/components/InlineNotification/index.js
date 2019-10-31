import React from 'react';
import styled from 'react-emotion';
import { InlineNotification as Inline } from 'carbon-components-react';

const CustomInlineNotification = styled(Inline)`
  background-color: #666666;
  align-items: center;
  display: flex;
  margin: 0;
  bottom: 20px;
  right: 20px;
  position: fixed;
  z-index: 100;

  .bx--inline-notification__text-wrapper {
    p,
    .bx--inline-notification__subtitle {
      color: #ffffff;
    }
  }

  .bx--inline-notification__close-icon {
    fill: #ffffff;
  }
`;

function InlineNotification(props) {
  return <CustomInlineNotification {...props} />;
}

export default InlineNotification;
