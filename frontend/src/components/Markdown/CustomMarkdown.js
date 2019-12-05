import React from 'react';
import Markdown from 'react-markdown';
import htmlParser from 'react-markdown/plugins/html-parser';
import styled from 'react-emotion';

const parseHtml = htmlParser({
  isValidNode: node => node.type !== 'script',
});

const MarkdownContainer = styled('div')`
  margin-bottom: ${({ marginBottom }) => marginBottom && '2rem'};
  h1,
  h2,
  h3,
  h4 {
    margin: 10px 0;
    font-weight: bold;
    color: ${({ light }) => light && '#fff'};
  }
  p {
    padding: 0px;
    line-height: 1.6;
    color: ${({ light }) => light && '#fff'};
    padding-left: ${({ paddingLeft }) => paddingLeft && '2rem'};
    margin-bottom: 15px;
  }
  ol {
    list-style: decimal;
    color: ${({ light }) => light && '#fff'};
  }
  ul {
    list-style: disc;
    color: ${({ light }) => light && '#fff'};
  }
  li {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 20px;
    line-height: 2;
    color: ${({ light }) => light && '#fff'};
  }
  img {
    width: 100%;
    margin: 20px 0;
    color: ${({ light }) => light && '#fff'};
  }
`;

const CustomMarkdown = ({
  source,
  renderers,
  light,
  paddingLeft,
  marginBottom,
}) => (
  <MarkdownContainer
    light={light}
    paddingLeft={paddingLeft}
    marginBottom={marginBottom}
  >
    <Markdown
      source={source}
      renderers={renderers}
      escapeHtml={false}
      astPlugins={[parseHtml]}
    />
  </MarkdownContainer>
);

export default CustomMarkdown;
