// @flow
import React, { Component } from 'react';
import CircularProgressbar from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { detect } from 'detect-browser';

const browser = detect();

type Props = {
  startTime: number, // Date.now() ms at start
  countdown: number, // delta in seconds
  onTimeout: () => void,
};

type State = {
  currentTime: number,
};

type CircularProgressbarProps = {
  text: *,
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
    ? `${Math.ceil(secondsRemaining)}s`
    : `${Math.ceil(secondsRemaining / 60)}m`;

class StopClock extends Component<Props, State> {
  timer: ?IntervalID;

  state: State = {
    currentTime: Date.now(),
  };

  componentDidMount() {
    this.endTime = this.props.startTime + 1000 * this.props.countdown;
    this.timer = setInterval(this.tick, 500);
  }

  componentDidUpdate() {
    if (this.endTime !== 0 && Date.now() >= this.endTime) {
      this.timer && clearInterval(this.timer);
      this.endTime = 0;
      this.props.onTimeout();
    }
  }

  componentWillUnmount() {
    this.timer && clearInterval(this.timer);
  }

  endTime: number = 0;

  tick = () => {
    this.setState({
      currentTime: Date.now(),
    });
  };

  render() {
    const { currentTime } = this.state;
    const { startTime, countdown } = this.props;
    const percentage = getPercRemaining(currentTime, startTime, countdown);

    return (
      this.endTime !== 0 && (
        <StyledCircularProgressbar
          text={
            <tspan dy={browser.name === 'ie' ? 8 : 0}>
              {getTimeLabel(countdown - percentage * countdown)}
            </tspan>
          }
          percentage={percentage * 100}
        />
      )
    );
  }
}

export default StopClock;
