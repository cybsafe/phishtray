//@flow
import React, { Fragment, useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import moment from 'moment';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faThumbsUp,
  faThumbsDown,
  faArrowDown,
  faArrowUp,
} from '@fortawesome/free-solid-svg-icons';

import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import {
  Container,
  EmailItemField,
  EmailItemContent,
  Emphasis,
  Title,
  ButtonsContainer,
  AppButton,
  BehaviorFieldSuccess,
  BehaviorFieldNegative,
  SeeDetails,
} from './ui';
import WideHeader from '../../components/Header/WideHeader';
import { negativeMessages, positiveMessages, sanitizeActions } from './utils';
import withErrorBoundary from '../../errors/ErrorBoundary';

type Props = {
  history: Object,
  match: Object,
  params: Object,
  participantUuid: string,
};

function PhishingEmailInfo({
  history,
  match: {
    params: { participantUuid },
  },
}: Props) {
  const phishingEmails = useSelector(state => state.debrief.phishingEmails);
  const dispatch = useDispatch();
  const [isShowing, setIsShowing] = useState(false);
  const [page, setPage] = useState(0);

  useEffect(() => {
    dispatch(getDebrief(participantUuid));
  }, [participantUuid, dispatch]);

  const nextPage = (page, max) => {
    if (page > max - 2) return false;
    setIsShowing(false);
    setPage(page + 1);
  };

  const prevPage = page => {
    if (page <= 0) return false;
    setIsShowing(false);
    setPage(page - 1);
  };

  const showDetails = () => {
    setIsShowing(!isShowing);
  };

  if (phishingEmails[page] === undefined) {
    return false;
  }

  return (
    <Fragment>
      <WideHeader
        title="Thanks for taking the exercise"
        subtitle="Find out more"
      />
      <Container>
        <div>
          <Title>Phishing Email {page + 1}</Title>

          {phishingEmails[page].phishingExplained && (
            <EmailItemField>
              <EmailItemContent>
                <Emphasis>Description:</Emphasis>{' '}
                {phishingEmails[page].phishingExplained}
              </EmailItemContent>
            </EmailItemField>
          )}

          <EmailItemField>
            <EmailItemContent>
              <Emphasis>From:</Emphasis> {phishingEmails[page].fromAddress}
            </EmailItemContent>

            <EmailItemContent>
              <Emphasis>Subject:</Emphasis> {phishingEmails[page].subject}
            </EmailItemContent>

            <EmailItemContent>
              <Emphasis>Body:</Emphasis>
              {phishingEmails[page].content}
            </EmailItemContent>
          </EmailItemField>

          {phishingEmails[page].participantActions.length > 0 && (
            <SeeDetails kind="secondary" onClick={() => showDetails()}>
              See details{' '}
              <FontAwesomeIcon icon={isShowing ? faArrowUp : faArrowDown} />
            </SeeDetails>
          )}

          {isShowing && phishingEmails[page].participantActions.length > 0 && (
            <EmailItemField>
              {phishingEmails &&
                phishingEmails[page].participantActions.map((info, i) => (
                  <EmailItemContent
                    fault={
                      info.actionId ===
                        phishingEmails[page].participantBehaviour.actionId &&
                      'fault'
                    }
                    key={info.actionId}
                  >
                    {moment(info.timestamp).format('h:mm:ss a')} -{' '}
                    {sanitizeActions(info.actionType)}
                  </EmailItemContent>
                ))}
            </EmailItemField>
          )}

          {phishingEmails[page].participantBehaviour.behaviour ===
            'negative' && (
            <BehaviorFieldNegative>
              <FontAwesomeIcon icon={faThumbsDown} />
              {negativeMessages(
                phishingEmails[page].participantActions[1].actionType
              )}
            </BehaviorFieldNegative>
          )}

          {phishingEmails[page].participantBehaviour.behaviour ===
            'positive' && (
            <BehaviorFieldSuccess>
              <FontAwesomeIcon icon={faThumbsUp} />
              {positiveMessages(
                phishingEmails[page].participantActions[1].actionType
              )}
            </BehaviorFieldSuccess>
          )}
        </div>

        <ButtonsContainer>
          {page > 0 && (
            <AppButton onClick={() => prevPage(page)}>
              Previous E-mail
            </AppButton>
          )}

          {page < phishingEmails.length - 1 && (
            <AppButton onClick={() => nextPage(page, phishingEmails.length)}>
              Next Email
            </AppButton>
          )}

          {page === phishingEmails.length - 1 && (
            <AppButton
              onClick={() => history.push(`/training/${participantUuid}`)}
            >
              More Information
            </AppButton>
          )}
        </ButtonsContainer>
      </Container>
    </Fragment>
  );
}

export default withErrorBoundary(PhishingEmailInfo);
