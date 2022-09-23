import { MockedProvider } from '@apollo/react-testing';
import { act } from '@testing-library/react';
import React from 'react';
import wait from 'waait';
import { fakeApolloAllCommunicationMessages } from '../../../../fixtures/communication/fakeApolloAllCommunicationMessages';
import { ApolloLoadingLink, render } from '../../../testUtils/testUtils';
import { FeedbackTable } from './FeedbackTable';

describe('containers/tables//Feedback/FeedbackTable', () => {
  it('should render with data', async () => {
    const { container } = render(
      <MockedProvider
        addTypename={false}
        mocks={fakeApolloAllCommunicationMessages}
      >
        <FeedbackTable
          filter={{
            search: '',
            status: '',
            createdBy: '',
            createdAtRange: '',
          }}
          businessArea={'afghanistan'}
        />
      </MockedProvider>,
    );
    await act(() => wait(0)); // wait for response

    expect(container).toMatchSnapshot();
  });

  it('should render loading', () => {
    const { container } = render(
      <MockedProvider
        link={new ApolloLoadingLink()}
        addTypename={false}
        mocks={fakeApolloAllCommunicationMessages}
      >
        <FeedbackTable
          filter={{
            search: '',
            status: '',
            createdBy: '',
            createdAtRange: '',
          }}
          businessArea={'afghanistan'}
        />
      </MockedProvider>,
    );

    expect(container).toMatchSnapshot();
  });
});
