import styled from 'styled-components';
import TableCell from '@material-ui/core/TableCell';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { PaymentRecordNode } from '../../../__generated__/graphql';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { ClickableTableRow } from '../../../components/table/ClickableTableRow';
import { StatusBox } from '../../../components/StatusBox';
import {
  formatCurrencyWithSymbol,
  paymentRecordStatusToColor,
} from '../../../utils/utils';
import { UniversalMoment } from '../../../components/UniversalMoment';
import { AnonTableCell } from '../../../components/table/AnonTableCell';

const StatusContainer = styled.div`
  min-width: 120px;
  max-width: 200px;
`;

interface PaymentRecordTableRowProps {
  paymentRecord: PaymentRecordNode;
  openInNewTab: boolean;
}

export function PaymentRecordTableRow({
  paymentRecord,
  openInNewTab,
}: PaymentRecordTableRowProps): React.ReactElement {
  const businessArea = useBusinessArea();
  const history = useHistory();
  const handleClick = (): void => {
    const path = `/${businessArea}/payment-records/${paymentRecord.id}`;
    if (openInNewTab) {
      window.open(path);
    } else {
      history.push(path);
    }
  };
  return (
    <ClickableTableRow
      hover
      onClick={handleClick}
      role='checkbox'
      key={paymentRecord.id}
    >
      <TableCell align='left'>{paymentRecord.caId}</TableCell>
      <TableCell align='left'>
        <StatusContainer>
          <StatusBox
            status={paymentRecord.status}
            statusToColor={paymentRecordStatusToColor}
          />
        </StatusContainer>
      </TableCell>
      <AnonTableCell>{paymentRecord.headOfHousehold?.fullName}</AnonTableCell>
      <TableCell align='left'>{paymentRecord.household.unicefId}</TableCell>
      <TableCell align='left'>{paymentRecord.household.size}</TableCell>
      <TableCell align='right'>
        {formatCurrencyWithSymbol(
          paymentRecord.entitlementQuantity,
          paymentRecord.currency,
        )}
      </TableCell>
      <TableCell align='right'>
        {formatCurrencyWithSymbol(
          paymentRecord.deliveredQuantity,
          paymentRecord.currency,
        )}
      </TableCell>
      <TableCell align='right'>
        <UniversalMoment>{paymentRecord.deliveryDate}</UniversalMoment>
      </TableCell>
    </ClickableTableRow>
  );
}
