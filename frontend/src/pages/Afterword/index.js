// @flow
import React from 'react';
import { connect } from 'react-redux';
import ReactMarkdown from 'react-markdown';
import styled from 'react-emotion';
import { DataTable } from 'carbon-components-react';
import { persistor } from '../../redux';
import { getRange, HOST_BACKEND } from '../../utils';

const {
  Table,
  TableHead,
  TableHeader,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
} = DataTable;

const Container = styled('div')({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100%',
  backgroundColor: '#fff',
  boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)',
  padding: '1rem',
  flexDirection: 'column',
});

const MarkdownContainer = styled('div')({
  margin: '0px 0px 15px',
});

const ContentContainer = styled('div')({
  width: '60%',
  maxWidth: '800px',
});

const Title = styled('h1')({
  display: 'block',
  fontSize: ' 2.25rem',
  lineHeight: 1.25,
  marginBottom: '35px',
  fontWeight: 300,
  margin: '0px 0px 15px',
});

type Props = {
  afterwordMessage: string,
  match: any,
};

const clearSessionStorage = async () => await sessionStorage.clear();

const MarginBottomParagraph = styled('p')`
  margin-bottom: 30px;
`;

type State = {
  scores: Array<any>,
};

type ParticipantScore = {
  task: string,
  score: number,
  debrief: string,
};

type ParticipantScores = {
  id: string,
  scores: ParticipantScore[],
};

class Afterword extends React.Component<Props, State> {
  state: State = {
    scores: [],
  };

  componentDidMount() {
    getRange(0, 100).map(i => clearInterval(i)); //not the best solution
    clearSessionStorage().then(() => {
      persistor.purge();
    });
    const { participantUuid } = this.props.match.params;
    const apiUrl = `${HOST_BACKEND}/api/v1/participant-scores/${participantUuid}`;
    fetch(apiUrl).then((response: ParticipantScores) => {
      if ('scores' in response) {
        this.setState({
          scores: response.scores,
        });
      }
    });
  }

  getHeaders = () => [
    { key: 'task', header: 'Task' },
    { key: 'score', header: 'Score' },
    { key: 'debrief', header: 'Message' },
  ];

  render() {
    return (
      <Container>
        <ContentContainer>
          <Title>Thanks for taking the exercise.</Title>
          <MarginBottomParagraph>
            The exercise you have just taken part in is designed to assess the
            decision-making process of planning, coordinating and uncertainty
            management. If you have completed the exercise in full you will find
            an automated report below which describes your strengths and areas
            for improvements associated with these skills.
          </MarginBottomParagraph>
          {this.props.afterwordMessage && (
            <MarkdownContainer>
              <ReactMarkdown source={this.props.afterwordMessage} />
            </MarkdownContainer>
          )}
          {this.state.scores && (
            <DataTable
              rows={this.state.scores}
              headers={this.getHeaders()}
              render={({ rows, headers, getHeaderProps }) => {
                return (
                  <TableContainer title="Debrief">
                    <Table>
                      <TableHead>
                        <TableRow>
                          {headers.map((header, index) => (
                            <TableHeader
                              // eslint-disable-next-line react/no-array-index-key
                              key={`${index}-${header.header}`}
                              {...getHeaderProps({ header })}
                            >
                              {header.header}
                            </TableHeader>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {rows.map((row, index) => (
                          // eslint-disable-next-line react/no-array-index-key
                          <TableRow key={index}>
                            {row.cells.map(cell => (
                              <TableCell key={cell.id}>{cell.value}</TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                );
              }}
            />
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
)(Afterword);
