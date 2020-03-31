// @flow
import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';
import styled from 'react-emotion';
import {
  StructuredListWrapper,
  StructuredListHead,
  StructuredListBody,
  StructuredListRow,
  StructuredListCell,
  Button as CarbonButton,
} from 'carbon-components-react';
import WideHeader from '../../components/Header/WideHeader';
import { persistor } from '../../redux';
import { getRange } from '../../utils';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';
import CustomMarkdown from '../../components/Markdown/CustomMarkdown';
import withErrorBoundary from '../../errors/ErrorBoundary';

const Container = styled('div')`
  display: flex;
  align-items: center;
  min-height: 100%;
  background-color: #fff;
  flex-direction: column;
`;

const ContentContainer = styled('div')`
  max-width: 1000px;
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 3rem;
  margin-bottom: 3rem;
`;

const DebriefTitle = styled('h5')`
  font-size: 1.2rem;
  padding-left: 2rem;
  margin-bottom: 1rem;
`;

const List = styled(StructuredListWrapper)`
  margin-bottom: 3rem;
`;

const ListRow = styled(StructuredListRow)`
  border: 0px !important;
  &:hover {
    background-color: ${({ head }) => (head ? 'none' : 'rgba(13,121,205,0.1)')};
    box-shadow: ${({ head }) => (head ? 'none' : 'inset 0 0 2px #0D79CD')};
  }
`;

const ListCell = styled(StructuredListCell)`
  padding-left: 2rem !important;
  font-size: ${({ head }) => (head ? '1.2rem' : 'inherit')};
`;

const Button = styled(CarbonButton)`
  margin-right: 2rem;
  align-self: flex-end;
`;

type Props = {
  match: any,
  history: *,
};

const clearSessionStorage = async () => await sessionStorage.clear();

const Afterword = ({ match, history }: Props) => {
  const { participantUuid } = match.params;
  const { debrief, scores } = useSelector(state => state.debrief);
  const afterwordMessage = useSelector(state => state.exercise.afterword);
  const dispatch = useDispatch();
  const getHeaders = () => [
    { key: 'task', header: 'Task' },
    { key: 'score', header: 'Score' },
    { key: 'debrief', header: 'Message' },
  ];

  useEffect(() => {
    async function didMount() {
      getRange(0, 100).map(i => clearInterval(i)); //not the best solution
      await clearSessionStorage();
      await persistor.purge();
      dispatch(getDebrief(participantUuid));
    }
    didMount();
  }, [dispatch, participantUuid]);

  return (
    <Container>
      <WideHeader title="Thanks for taking the exercise." />
      <ContentContainer>
        {afterwordMessage && (
          <>
            <DebriefTitle>Debrief</DebriefTitle>
            <CustomMarkdown
              source={afterwordMessage}
              marginBottom
              paddingLeft
            />
          </>
        )}
        {scores && (
          <List>
            <StructuredListHead>
              <ListRow head>
                {getHeaders().map((header, index) => (
                  <ListCell key={`${index}-${header.header}`} head>
                    {header.header}
                  </ListCell>
                ))}
              </ListRow>
            </StructuredListHead>
            <StructuredListBody>
              {scores.map((row, index) => (
                <ListRow key={`${index}-${row.task}`}>
                  <ListCell>{row.task}</ListCell>
                  <ListCell>{row.score}</ListCell>
                  <ListCell>{row.debrief}</ListCell>
                </ListRow>
              ))}
            </StructuredListBody>
          </List>
        )}
        {debrief && (
          <Button onClick={() => history.push(`/debrief/${participantUuid}`)}>
            Find out more
          </Button>
        )}
      </ContentContainer>
    </Container>
  );
};

export default withErrorBoundary(withRouter(Afterword));
