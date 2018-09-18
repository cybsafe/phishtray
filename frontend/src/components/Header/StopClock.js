// @flow
import React, { Component } from 'react';
import CircularProgressbar from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

type Props = {
  startTime: number, // Date.now() ms at start
  countdown: number, // delta in seconds
  currentTime: number, // Date.now() at present
  history: *,
};

type State = {
  currentTime: number,
};

type CircularProgressbarProps = {
  text: string,
  percentage: number,
};

const StyledCircularProgressbar = (props: CircularProgressbarProps) => (
  <CircularProgressbar
    percentage={props.percentage}
    text={props.text}
    strokeWidth={10}
    styles={{
      root: {},
      path: {
        stroke: '#1c8bf4',
        strokeLinecap: 'butt',
        transition: 'stroke-dashoffset 0.5s ease 0s',
      },
      trail: {
        stroke: '#e6e6e6',
      },
      text: {
        fill: '#1c8bf4',
        fontSize: '30px',
      },
    }}
  />
);

const getPercRemaining = (
  currentTime: number,
  startTime: number,
  countdown: number
) => {
  return (currentTime - startTime) / (countdown * 1000);
};

const getTimeLabel = (secondsRemaining: number) =>
  secondsRemaining < 60
    ? `${Math.round(secondsRemaining)}s`
    : `${Math.round(secondsRemaining / 60)}m`;

class StopClock extends Component<Props, State> {
  state: State = {
    currentTime: Date.now(),
  };

  tick = () => {
    this.setState({
      currentTime: Date.now(),
    });
  };

  timer = null;
  endTime = 0;
  componentDidMount() {
    this.timer = setInterval(this.tick, 500);
    this.endTime = this.props.startTime + 1000 * this.props.countdown;
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  render() {
    const { currentTime } = this.state;
    if (this.endTime !== 0 && currentTime >= this.endTime) {
      this.props.history.push('/welcome');
    }
    const { startTime, countdown } = this.props;
    const percentage = getPercRemaining(currentTime, startTime, countdown);
    return startTime > 0 ? (
      <StyledCircularProgressbar
        text={getTimeLabel(countdown - percentage * countdown)}
        percentage={percentage * 100}
      />
    ) : null;
  }
}

export default StopClock;
