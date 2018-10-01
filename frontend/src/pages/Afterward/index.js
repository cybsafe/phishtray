import React from 'react';
import { connect } from 'react-redux';

const Afterward = () => {
  return <div>Thanks for taking the exercise</div>;
};

export default connect(
  state => ({
    state: state,
  }),
  {}
)(Afterward);
