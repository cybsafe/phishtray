//@flow
import React, { Fragment, useEffect, useState } from 'react';
import { connect } from 'react-redux';
import moment from 'moment';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faThumbsUp,
  faThumbsDown,
  faArrowDown,
  faArrowUp,
} from '@fortawesome/free-solid-svg-icons';

import {
  Container,
  EmailItem,
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

type Props = {
  phishingEmails: [*],
  history: Object,
  getDebrief: (id: string) => void,
  match: Object,
  params: Object,
  participantUuid: string,
};

function PhishingEmailInfo({
  phishingEmails,
  history,
  getDebrief,
  match: {
    params: { participantUuid },
  },
}: Props) {
  const [hasPrevious, setHasPrevious] = useState(false);
  const [isShowing, setIsShowing] = useState(false);
  const [nextLink, setNextLink] = useState(false);
  const [hasNext, setHasNext] = useState(true);
  const [page, setPage] = useState(0);

  useEffect(() => {
    getDebrief(participantUuid);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    page > 0 ? setHasPrevious(true) : setHasPrevious(false);
  }, [page]);

  useEffect(() => {
    page < phishingEmails.length - 1 ? setHasNext(true) : setHasNext(false);
  }, [page, phishingEmails]);

  useEffect(() => {
    page === phishingEmails.length - 1 ? setNextLink(true) : setNextLink(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page]);

  const nextPage = (visible, max) => {
    if (page > max - 2) return false;
    setPage(page + 1);
    setIsShowing(false);
  };

  const prevPage = page => {
    if (page <= 0) return false;
    setPage(page - 1);
    setIsShowing(false);
  };

  const showDetails = () => {
    setIsShowing(!isShowing);
  };

  if (phishingEmails[page] === undefined) {
    return false;
  }

  const output = phishingEmails.map(obj => {
    return Object.keys(obj)
      .sort()
      .map(key => {
        return obj[key];
      });
  });

  const behaviorCondition = phishingEmails && output[page][4];

  return (
    <Fragment>
      <WideHeader
        title="Thanks for taking the exercise"
        subtitle="Find out more"
      />
      <Container>
        <div>
          <Title>Phishing Email {page + 1}</Title>
          <EmailItemField>
            <EmailItemContent>
              <Emphasis>Description:</Emphasis> Description
            </EmailItemContent>
          </EmailItemField>

          <EmailItemField>
            <EmailItemContent>
              <Emphasis>To:</Emphasis> {phishingEmails && output[page][1]}
            </EmailItemContent>

            <EmailItemContent>
              <Emphasis>Subject:</Emphasis> {phishingEmails && output[page][6]}
            </EmailItemContent>

            <EmailItemContent>
              <Emphasis>Body:</Emphasis>
              {phishingEmails && output[page][0]}
            </EmailItemContent>
          </EmailItemField>

          <SeeDetails kind="secondary" onClick={() => showDetails()}>
            See details{' '}
            <FontAwesomeIcon icon={isShowing ? faArrowUp : faArrowDown} />
          </SeeDetails>

          {isShowing && (
            <EmailItemField>
              {phishingEmails &&
                output[page][3].length &&
                output[page][3].map(info => (
                  <EmailItemContent key={info.actionType}>
                    {moment(info.timestamp).format('h:mm:ss a')} -{' '}
                    {sanitizeActions(info.actionType)}
                  </EmailItemContent>
                ))}
            </EmailItemField>
          )}

          {behaviorCondition === 'negative' && (
            <BehaviorFieldNegative>
              <FontAwesomeIcon icon={faThumbsDown} />
              {negativeMessages(output[page][3][1].actionType)}
            </BehaviorFieldNegative>
          )}

          {behaviorCondition === 'positive' && (
            <BehaviorFieldSuccess>
              <FontAwesomeIcon icon={faThumbsUp} />
              {positiveMessages(output[page][3][1].actionType)}
            </BehaviorFieldSuccess>
          )}
        </div>

        <ButtonsContainer>
          {hasPrevious && (
            <AppButton onClick={() => prevPage(page)}>
              Previous E-mail
            </AppButton>
          )}

          {hasNext && (
            <AppButton onClick={() => nextPage(page, phishingEmails.length)}>
              Next Email
            </AppButton>
          )}

          {nextLink && (
            <AppButton
              onClick={() => history.push(`/training/${participantUuid}`)}
            >
              More Informations
            </AppButton>
          )}
        </ButtonsContainer>
      </Container>
    </Fragment>
  );
}

const mapStateToProps = state => ({
  phishingEmails: state.debrief.phishingEmails,
});

const mapDispatchToProps = {
  getDebrief,
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PhishingEmailInfo);
