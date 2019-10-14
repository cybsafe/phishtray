// @flow

import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { Button as CarbonButton } from 'carbon-components-react';

const CopyButton = ({ copyText }: { copyText: string }) => (
  <CarbonButton kind="secondary">
    <CopyToClipboard text={copyText}>
      <FontAwesomeIcon icon={faCopy} />
    </CopyToClipboard>
  </CarbonButton>
);

export default CopyButton;
