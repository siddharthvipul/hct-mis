import TableCell from '@material-ui/core/TableCell';
import styled from 'styled-components';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { ClickableTableRow } from '../../core/Table/ClickableTableRow';
import { StatusBox } from '../../core/StatusBox';
import {
  grievanceTicketStatusToColor,
  renderUserName,
} from '../../../utils/utils';
import { UniversalMoment } from '../../core/UniversalMoment';
import { AllGrievanceTicketQuery } from '../../../__generated__/graphql';
import { BlackLink } from '../../core/BlackLink';

const StatusContainer = styled.div`
  min-width: 120px;
  max-width: 200px;
`;

interface GrievancesTableRowProps {
  ticket: AllGrievanceTicketQuery['allGrievanceTicket']['edges'][number]['node'];
  statusChoices: { [id: number]: string };
  categoryChoices: { [id: number]: string };
  canViewDetails: boolean;
}

export function GrievancesTableRow({
  ticket,
  statusChoices,
  categoryChoices,
  canViewDetails,
}: GrievancesTableRowProps): React.ReactElement {
  const history = useHistory();
  const businessArea = useBusinessArea();
  const detailsPath = `/${businessArea}/grievance-and-feedback/${ticket.id}`;

  const handleClick = (): void => {
    history.push(detailsPath);
  };
  return (
    <ClickableTableRow
      hover
      onClick={canViewDetails ? handleClick : undefined}
      role='checkbox'
      key={ticket.id}
    >
      <TableCell align='left'>
        {canViewDetails ? (
          <BlackLink to={detailsPath}>{ticket.unicefId}</BlackLink>
        ) : (
          ticket.unicefId
        )}
      </TableCell>
      <TableCell align='left'>
        <StatusContainer>
          <StatusBox
            status={statusChoices[ticket.status]}
            statusToColor={grievanceTicketStatusToColor}
          />
        </StatusContainer>
      </TableCell>
      <TableCell align='left'>{renderUserName(ticket.assignedTo)}</TableCell>
      <TableCell align='left'>{categoryChoices[ticket.category]}</TableCell>
      <TableCell align='left'>{ticket.household?.unicefId || '-'}</TableCell>
      <TableCell align='left'>
        <UniversalMoment>{ticket.createdAt}</UniversalMoment>
      </TableCell>
      <TableCell align='left'>
        <UniversalMoment>{ticket.userModified}</UniversalMoment>
      </TableCell>
    </ClickableTableRow>
  );
}