import React from 'react';
import styled from 'styled-components';
import { UniversalTable } from '../../../containers/tables/UniversalTable';
import { decodeIdString, reduceChoices } from '../../../utils/utils';
import {
  AllGrievanceTicketQuery,
  AllGrievanceTicketQueryVariables,
  useAllGrievanceTicketQuery,
  useGrievancesChoiceDataQuery,
} from '../../../__generated__/graphql';
import { LoadingComponent } from '../../LoadingComponent';
import { headCells } from './GrievancesTableHeadCells';
import { GrievancesTableRow } from './GrievancesTableRow';

const TableWrapper = styled.div`
  padding: 20px;
`;

interface GrievancesTableProps {
  businessArea: string;
  filter;
}

export const GrievancesTable = ({
  businessArea,
  filter,
}: GrievancesTableProps): React.ReactElement => {
  const initialVariables: AllGrievanceTicketQueryVariables = {
    businessArea,
    search: filter.search,
    status: [filter.status],
    fsp: [filter.fsp],
    createdAtRange: JSON.stringify(filter.createdAtRange),
    admin: [decodeIdString(filter?.admin?.node?.id)],
  };

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useGrievancesChoiceDataQuery();
  if (choicesLoading) return <LoadingComponent />;
  if (!choicesData) return null;

  const statusChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketStatusChoices);

  const categoryChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketCategoryChoices);

  return (
    <TableWrapper>
      <UniversalTable<
        AllGrievanceTicketQuery['allGrievanceTicket']['edges'][number]['node'],
        AllGrievanceTicketQueryVariables
      >
        headCells={headCells}
        title='Grievance and Feedback List'
        rowsPerPageOptions={[10, 15, 20]}
        query={useAllGrievanceTicketQuery}
        queriedObjectName='allGrievanceTicket'
        initialVariables={initialVariables}
        renderRow={(row) => (
          <GrievancesTableRow
            key={row.id}
            ticket={row}
            statusChoices={statusChoices}
            categoryChoices={categoryChoices}
          />
        )}
      />
    </TableWrapper>
  );
};
