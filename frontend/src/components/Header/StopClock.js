// @flow
import React from 'react';
import CircularProgressbar from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

type Props = {
  startTime: number, // Date.now() ms at start
  countdown: number, // delta in seconds
  currentTime: number, // Date.now() at present
};

type CircularProgressbarProps = {
  text: string,
  percentage: number,
};

const StyledCircularProgressbar = (props: CircularProgressbarProps) =>
  props.startTime > 0 ? (
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
  ) : null;

const getPercRemaining = ({ currentTime, startTime, countdown }: Props) => {
  return (currentTime - startTime) / (countdown * 1000);
};

const getTimeLabel = (secondsRemaining: number) =>
  `${Math.ceil(secondsRemaining / 60)}m`;

const StopClock = (props: Props) => {
  const percentage = getPercRemaining(props);
  return (
    <StyledCircularProgressbar
      text={getTimeLabel(props.countdown - percentage * props.countdown)}
      percentage={percentage * 100}
    />
  );
};

export default StopClock;
