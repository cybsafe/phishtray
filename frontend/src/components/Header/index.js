// @flow
import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import { Button, Modal } from 'carbon-components-react';
import StopClock from './StopClock';
import { logAction, getHeaderText } from '../../utils';
import actionTypes from '../../config/actionTypes';
import { resetCountdown } from '../../actions/exerciseActions';

const SectionHeader = styled('div')({
  display: 'flex',
  flex: 0,
  flexBasis: 280,
  borderTopRightRadius: '5px',
  alignItems: 'center',
  justifyContent: 'center',
  marginBottom: '-1px',
});

const HeaderText = styled('h2')({
  textTransform: 'uppercase',
  color: '#e6e6e6',
  fontSize: 18,
  letterSpacing: '1.4px',
});

const ClockContainer = styled('div')({
  flex: 1,
  textAlign: 'right',
});

const ButtonContainer = styled('div')({
  flex: 1,
  maxWidth: '100px',
});

const buttonProps = {
  className: css({ display: 'flex', flexGrow: 1, marginTop: '20px' }),
  id: 'test2',
  kind: 'secondary',
};

const confirmationProps = {
  shouldSubmitOnEnter: false,
  modalHeading: 'Confirm Exit',
  primaryButtonText: 'Yes, I would like to Exit',
  secondaryButtonText: 'Cancel',
  iconDescription: 'Close',
};

const ConfirmationModal = ({ visible, ...rest }) => (
  <Modal {...confirmationProps} open={visible} {...rest}>
    <p className="bx--modal-content__text">Are you sure you want to exit?</p>
  </Modal>
);

type Props = {
  startTime: number,
  countdownMins: number,
  match: *,
  history: *,
  location: *,
  exerciseId: string,
  participantId: string,
  resetCountdown: () => void,
};

const getHeader = location => (
  <SectionHeader className={css({ backgroundColor: '#1C8BF4' })}>
    <HeaderText>{getHeaderText(location)}</HeaderText>
  </SectionHeader>
);

class Header extends Component<Props> {
  state = {
    modalOpen: false,
  };

  render() {
    const clearSessionStorage = async () => await sessionStorage.clear();
    return (
      <div
        className={css({
          display: 'flex',
          flexDirection: 'row',
          height: 80,
          borderBottom: '1px solid #e6e6e6',
          backgroundColor: '#fff',
        })}
      >
        <div
          className={css({
            height: 80,
            width: 160,
            backgroundColor: '#1D1B1C',
          })}
        />
        {getHeader(this.props.location.pathname)}
        <ClockContainer>
          <div
            style={{
              width: '60px',
              paddingTop: '10px',
              marginRight: '20px',
              display: 'inline-block',
            }}
          >
            <StopClock
              startTime={this.props.startTime}
              countdown={this.props.countdownMins * 60}
              onTimeout={() => {
                logAction({
                  participantId: this.props.participantId,
                  actionType: actionTypes.experimentEndTimeout,
                  timestamp: new Date(),
                  timeDelta: Date.now() - this.props.startTime,
                });
                clearSessionStorage()
                  .then(() => {
                    this.props.resetCountdown();
                    this.props.history.push(
                      `/afterword/${this.props.participantId}`
                    );
                  })
                  .catch(e => console.error('error clearing your session', e));
              }}
            />
          </div>
        </ClockContainer>
        <ButtonContainer>
          <Button
            {...buttonProps}
            onClick={() => {
              this.setState({
                modalOpen: true,
              });
            }}
          >
            Exit
          </Button>
        </ButtonContainer>

        <ConfirmationModal
          visible={this.state.modalOpen}
          onRequestClose={() => this.setState({ modalOpen: false })}
          onSecondarySubmit={() => this.setState({ modalOpen: false })}
          onRequestSubmit={() => {
            logAction({
              participantId: this.props.participantId,
              actionType: actionTypes.experimentEndManual,
              timestamp: new Date(),
              timeDelta: Date.now() - this.props.startTime,
            });
            clearSessionStorage()
              .then(() => {
                this.props.resetCountdown();
                this.props.history.push(
                  `/afterword/${this.props.participantId}`
                );
              })
              .catch(e => console.error('error clearing your session', e));
          }}
        />
      </div>
    );
  }
}

const mapStateToProps = reduxState => ({
  startTime: reduxState.exercise.startTime,
  countdownMins: reduxState.exercise.lengthMinutes,
  participantId: reduxState.exercise.participant,
  exerciseId: reduxState.exercise.id,
});

export default connect(
  mapStateToProps,
  { resetCountdown }
)(withRouter(Header));
