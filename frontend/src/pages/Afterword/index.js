// @flow
import React from 'react';
import { connect } from 'react-redux';
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
import { getRange, HOST_BACKEND } from '../../utils';

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

const Description = styled('p')`
  font-size: 1rem;
  padding-left: 2rem;
  margin-bottom: 2rem;
`;

const List = styled(StructuredListWrapper)`
  margin-bottom: 3rem;
`;

const ListBody = styled(StructuredListBody)``;

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
  afterwordMessage: string,
  match: any,
  history: *,
  participantId: string,
};

const clearSessionStorage = async () => await sessionStorage.clear();

type State = {
  scores: Array<any>,
  debrief: boolean,
};

class Afterword extends React.Component<Props, State> {
  state: State = {
    scores: [],
    debrief: false,
  };

  async componentDidMount() {
    getRange(0, 100).map(i => clearInterval(i)); //not the best solution
    clearSessionStorage().then(() => {
      persistor.purge();
    });
    const { participantUuid } = this.props.match.params;
    const apiUrl = `${HOST_BACKEND}/api/v1/participant-scores/${participantUuid}`;
    const response = await fetch(apiUrl);
    const json = await response.json();
    const debrief = json.debrief;
    const scores =
      json.scores && json.scores.length > 0
        ? this.generateRows(json.scores)
        : [];
    this.setState({ scores, debrief });
  }

  generateRows = (data: []) =>
    data.map(row => {
      row.id = row.task;
      return row;
    });

  getHeaders = () => [
    { key: 'task', header: 'Task' },
    { key: 'score', header: 'Score' },
    { key: 'debrief', header: 'Message' },
  ];

  render() {
    const { afterwordMessage, participantId } = this.props;
    const { scores } = this.state;

    return (
      <Container>
        <WideHeader title="Thanks for taking the exercise." />
        <ContentContainer>
          {afterwordMessage && (
            <>
              <DebriefTitle>Debrief</DebriefTitle>
              <Description>{afterwordMessage}</Description>
            </>
          )}
          {scores && (
            <List>
              <StructuredListHead>
                <ListRow head>
                  {this.getHeaders().map((header, index) => (
                    <ListCell key={`${index}-${header.header}`} head>
                      {header.header}
                    </ListCell>
                  ))}
                </ListRow>
              </StructuredListHead>
              <ListBody>
                {scores.map((row, index) => (
                  <ListRow key={`${index}-${row.task}`}>
                    <ListCell>{row.task}</ListCell>
                    <ListCell>{row.score}</ListCell>
                    <ListCell>{row.debrief}</ListCell>
                  </ListRow>
                ))}
              </ListBody>
            </List>
          )}
          {this.state.debrief && (
            <Button
              onClick={() =>
                this.props.history.push(`/debrief/${participantId}`)
              }
            >
              Find out more
            </Button>
          )}
        </ContentContainer>
      </Container>
    );
  }
}

export default connect(
  state => ({
    score: 75,
    afterwordMessage: state.exercise.afterword,
  }),
  {}
)(withRouter(Afterword));
