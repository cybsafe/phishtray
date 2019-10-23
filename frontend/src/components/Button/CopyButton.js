// @flow

import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { Button as CarbonButton } from 'carbon-components-react';
import { connect } from 'react-redux';
import { setInlineNotification } from '../../actions/exerciseActions';

const CopyButton = ({
  copyText,
  setInlineNotification,
}: {
  copyText: string,
  setInlineNotification: (inlineNotification: string) => void,
}) => (
  <CopyToClipboard text={copyText}>
    <CarbonButton
      kind="secondary"
      onClick={() => setInlineNotification && setInlineNotification('copied')}
    >
      <FontAwesomeIcon icon={faCopy} />
    </CarbonButton>
  </CopyToClipboard>
);

export default connect(
  null,
  {
    setInlineNotification,
  }
)(CopyButton);
