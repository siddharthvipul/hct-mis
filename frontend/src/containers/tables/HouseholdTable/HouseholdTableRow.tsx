import TableCell from '@material-ui/core/TableCell';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from 'react-router-dom';
import { BlackLink } from '../../../components/BlackLink';
import { Flag } from '../../../components/Flag';
import { FlagTooltip } from '../../../components/FlagTooltip';
import { AnonTableCell } from '../../../components/table/AnonTableCell';
import { ClickableTableRow } from '../../../components/table/ClickableTableRow';
import { UniversalMoment } from '../../../components/UniversalMoment';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { choicesToDict, formatCurrencyWithSymbol } from '../../../utils/utils';
import {
  HouseholdChoiceDataQuery,
  HouseholdNode,
} from '../../../__generated__/graphql';

interface HouseHoldTableRowProps {
  household: HouseholdNode;
  choicesData: HouseholdChoiceDataQuery;
  canViewDetails: boolean;
}

export function HouseHoldTableRow({
  household,
  choicesData,
  canViewDetails,
}: HouseHoldTableRowProps): React.ReactElement {
  const history = useHistory();
  const { t } = useTranslation();
  const businessArea = useBusinessArea();
  const residenceStatusChoiceDict = choicesToDict(
    choicesData.residenceStatusChoices,
  );
  const householdDetailsPath = `/${businessArea}/population/household/${household.id}`;
  const handleClick = (): void => {
    history.push(householdDetailsPath);
  };
  return (
    <ClickableTableRow
      hover
      onClick={canViewDetails ? handleClick : undefined}
      role='checkbox'
      key={household.unicefId}
    >
      <TableCell align='left'>
        {household.hasDuplicates && (
          <FlagTooltip message={t('Possible Duplicates')} />
        )}
        {(household.sanctionListPossibleMatch ||
          household.sanctionListConfirmedMatch) && (
          <Flag
            message={t('Sanction List Confirmed Match')}
            confirmed={household.sanctionListConfirmedMatch}
          />
        )}
      </TableCell>
      <TableCell align='left'>
        <BlackLink to={householdDetailsPath}>{household.unicefId}</BlackLink>
      </TableCell>
      <AnonTableCell>{household.headOfHousehold.fullName}</AnonTableCell>
      <TableCell align='left'>{household.size}</TableCell>
      <TableCell align='left'>{household.admin2?.title || '-'}</TableCell>
      <TableCell align='left'>
        {residenceStatusChoiceDict[household.residenceStatus]}
      </TableCell>
      <TableCell align='right'>
        {formatCurrencyWithSymbol(
          household.totalCashReceived,
          household.currency,
        )}
      </TableCell>
      <TableCell align='right'>
        <UniversalMoment>{household.lastRegistrationDate}</UniversalMoment>
      </TableCell>
    </ClickableTableRow>
  );
}
