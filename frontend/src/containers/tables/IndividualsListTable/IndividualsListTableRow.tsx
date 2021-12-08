import { Box } from '@material-ui/core';
import TableCell from '@material-ui/core/TableCell';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useHistory } from 'react-router-dom';
import { BlackLink } from '../../../components/BlackLink';
import { FlagTooltip } from '../../../components/FlagTooltip';
import { WarningTooltip } from '../../../components/WarningTooltip';
import { LoadingComponent } from '../../../components/LoadingComponent';
import { AnonTableCell } from '../../../components/Table/AnonTableCell';
import { ClickableTableRow } from '../../../components/Table/ClickableTableRow';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { choicesToDict, sexToCapitalize } from '../../../utils/utils';
import {
  IndividualNode,
  useHouseholdChoiceDataQuery,
} from '../../../__generated__/graphql';

interface IndividualsListTableRowProps {
  individual: IndividualNode;
  canViewDetails: boolean;
}

export function IndividualsListTableRow({
  individual,
  canViewDetails,
}: IndividualsListTableRowProps): React.ReactElement {
  const history = useHistory();
  const businessArea = useBusinessArea();
  const { t } = useTranslation();
  const {
    data: choicesData,
    loading: choicesLoading,
  } = useHouseholdChoiceDataQuery();

  if (choicesLoading) {
    return <LoadingComponent />;
  }
  const relationshipChoicesDict = choicesToDict(
    choicesData.relationshipChoices,
  );

  const individualDetailsPath = `/${businessArea}/population/individuals/${individual.id}`;
  const handleClick = (): void => {
    history.push(individualDetailsPath);
  };

  let duplicateTooltip = null;
  if (individual.status === 'DUPLICATE') {
    duplicateTooltip = (
      <WarningTooltip confirmed message={t('Confirmed Duplicate')} />
    );
  } else if (individual.deduplicationGoldenRecordStatus !== 'UNIQUE') {
    duplicateTooltip = <WarningTooltip message={t('Possible Duplicate')} />;
  }
  return (
    <ClickableTableRow
      hover
      onClick={canViewDetails ? handleClick : undefined}
      role='checkbox'
      key={individual.id}
    >
      <TableCell align='left'>
        <>
          <Box mr={2}>{duplicateTooltip}</Box>
          <Box mr={2}>
            {individual.sanctionListPossibleMatch && (
              <FlagTooltip message={t('Sanction List Possible Match')} />
            )}
          </Box>
          <Box mr={2}>
            {individual.sanctionListConfirmedMatch && (
              <FlagTooltip
                message={t('Sanction List Confirmed Match')}
                confirmed
              />
            )}
          </Box>
        </>
      </TableCell>
      <TableCell align='left'>
        <BlackLink to={individualDetailsPath}>{individual.unicefId}</BlackLink>
      </TableCell>
      <AnonTableCell>{individual.fullName}</AnonTableCell>
      <TableCell align='left'>
        {individual.household ? individual.household.unicefId : ''}
      </TableCell>
      <TableCell align='left'>
        {relationshipChoicesDict[individual.relationship]}
      </TableCell>
      <TableCell align='right'>{individual.age}</TableCell>
      <TableCell align='left'>{sexToCapitalize(individual.sex)}</TableCell>
      <TableCell align='left'>{individual.household?.admin2?.title}</TableCell>
    </ClickableTableRow>
  );
}
