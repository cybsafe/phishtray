// @flow
import React from 'react';
import { connect } from 'react-redux';
import ReactMarkdown from 'react-markdown';
import styled from 'react-emotion';
import { DataTable } from 'carbon-components-react';
import { persistor } from '../../redux';
import { getRange } from '../../utils';

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
  afterwardMessage: String,
};

const clearSessionStorage = async () => await sessionStorage.clear();

const messageChecks = {
  planning75: 'planningGreaterthan75',
  planning: 'plasdsadsad',
  coordinate75: 'coordinate75',
  coordinate: 'coordinate',
  uncertainty75: 'uncertainty75',
  uncertainty: 'uncertainty',
};

class Afterward extends React.Component<Props> {
  state = {
    message: '',
  };

  componentDidMount() {
    getRange(0, 100).map(i => clearInterval(i)); //not the best solution
    clearSessionStorage().then(() => {
      persistor.purge();
    });
  }

  getDebriefText = check => {
    switch (check) {
      case messageChecks.planning75:
        return `You have demonstrated a strength in Planning and have communicated the goals and intent to others whilst listening to feedback. You have also taken account resources and time restrictions and dealt with uncertainty in the information.`;
      case messageChecks.planning:
        return `We have identified in this task that you have an area for development regarding Planning. On this occasion you may not have communicated the goals and intent to others as well as you could have, you may have missed some opportunities to gather feedback, or you may not have taken account of resources, time restrictions and uncertainty in the information.`;
      case messageChecks.coordinate:
        return `In completing this task, we have identified that Coordinating could be an area for development. You may have missed synchronising two or more people for an activity, and not taken the chance to build or maintain common ground.`;
      case messageChecks.coordinate75:
        return `You have demonstrated a strength in Coordinating by synchronising two or more people for an activity and establishing and maintaining common ground.`;
      case messageChecks.uncertainty75:
        return `You have demonstrated a strength in Uncertainty Management by identifying potential ambiguities and risks in the tasks, monitoring these risks and incorporating these into future decisions.`;
      case messageChecks.uncertainty:
        return `We have identified in that you have the potential to develop your Uncertainty Management. You may have missed identifying potential ambiguities and risks in the tasks, monitoring these risks, or not incorporated them into future decisions.`;
      default:
        return 'default';
    }
  };

  getInitialRows = () => {
    return [
      {
        id: 'a',
        name: 'Planning',
        message: this.getDebriefText(
          this.props.score <= 75
            ? messageChecks.planning75
            : messageChecks.planning
        ),
      },
      {
        id: 'b',
        name: 'Coordinating',
        message: this.getDebriefText(
          this.props.score >= 75
            ? messageChecks.coordinate75
            : messageChecks.coordinate
        ),
      },
      {
        id: 'c',
        name: 'Uncertainty Management',
        message: this.getDebriefText(
          this.props.score >= 75
            ? messageChecks.uncertainty75
            : messageChecks.uncertainty
        ),
      },
    ];
  };

  getHeaders = () => [
    { key: 'name', header: 'Task' },
    { key: 'message', header: 'Message' },
  ];

  render() {
    return (
      <Container>
        <ContentContainer>
          <Title>Thanks for taking the exercise.</Title>
          {this.props.afterwardMessage && (
            <MarkdownContainer>
              <ReactMarkdown source={this.props.afterwardMessage} />
            </MarkdownContainer>
          )}
          {this.props.score && (
            <DataTable
              rows={this.getInitialRows()}
              headers={this.getHeaders()}
              render={({ rows, headers, getHeaderProps }) => {
                return (
                  <TableContainer title="Debrief">
                    <Table>
                      <TableHead>
                        <TableRow>
                          {headers.map(header => (
                            <TableHeader {...getHeaderProps({ header })}>
                              {header.header}
                            </TableHeader>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {rows.map(row => (
                          <TableRow key={row.id}>
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
    afterwardMessage: state.exercise.afterword,
  }),
  {}
)(Afterward);
