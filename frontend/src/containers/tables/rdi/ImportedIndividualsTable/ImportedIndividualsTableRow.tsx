import TableCell from '@material-ui/core/TableCell';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { HouseholdChoiceDataQuery } from '../../../../__generated__/graphql';
import { BlackLink } from '../../../../components/core/BlackLink';
import { AnonTableCell } from '../../../../components/core/Table/AnonTableCell';
import { ClickableTableRow } from '../../../../components/core/Table/ClickableTableRow';
import { UniversalMoment } from '../../../../components/core/UniversalMoment';
import { DedupeResults } from '../../../../components/rdi/details/DedupeResults';
import { choicesToDict, sexToCapitalize } from '../../../../utils/utils';
<<<<<<< HEAD
import {
  HouseholdChoiceDataQuery,
  ImportedIndividualMinimalFragment,
} from '../../../../__generated__/graphql';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';
=======
>>>>>>> develop

interface ImportedIndividualsTableRowProps {
  individual;
  choices: HouseholdChoiceDataQuery;
  isMerged?: boolean;
}

export function ImportedIndividualsTableRow({
  individual,
  choices,
  isMerged,
}: ImportedIndividualsTableRowProps): React.ReactElement {
  const history = useHistory();
  const { baseUrl } = useBaseUrl();

  const relationshipChoicesDict = choicesToDict(choices.relationshipChoices);
  const roleChoicesDict = choicesToDict(choices.roleChoices);
  const deduplicationBatchDict = choicesToDict(
    choices.deduplicationBatchStatusChoices,
  );
  const deduplicationGoldenRecordDict = choicesToDict(
    choices.deduplicationGoldenRecordStatusChoices,
  );

<<<<<<< HEAD
  const individualPath = `/${baseUrl}/registration-data-import/individual/${individual.id}`;
=======
  const importedIndividualPath = `/${businessArea}/registration-data-import/individual/${individual.id}`;
  const mergedIndividualPath = `/${businessArea}/population/individuals/${individual.id}`;
  const url = isMerged ? mergedIndividualPath : importedIndividualPath;

>>>>>>> develop
  const handleClick = (e): void => {
    e.stopPropagation();
    history.push(url);
  };
  return (
    <ClickableTableRow
      hover
      onClick={(e) => handleClick(e)}
      role='checkbox'
      key={individual.id}
    >
      <TableCell align='left'>
        <BlackLink to={url}>
          {isMerged ? individual.unicefId : individual.importId}
        </BlackLink>
      </TableCell>
      <AnonTableCell>{individual.fullName}</AnonTableCell>
      <TableCell align='left'>{roleChoicesDict[individual.role]}</TableCell>
      <TableCell align='left'>
        {relationshipChoicesDict[individual.relationship]}
      </TableCell>
      <TableCell align='left'>
        <UniversalMoment>{individual.birthDate}</UniversalMoment>
      </TableCell>
      <TableCell align='left'>{sexToCapitalize(individual.sex)}</TableCell>
      <TableCell align='left'>
        {individual.deduplicationBatchResults.length ? (
          <>
            <DedupeResults
              isInBatch
              status={
                deduplicationBatchDict[individual.deduplicationBatchStatus]
              }
              results={individual.deduplicationBatchResults}
              individual={individual}
            />
          </>
        ) : (
          `${deduplicationBatchDict[individual.deduplicationBatchStatus]}`
        )}
      </TableCell>
      <TableCell align='left'>
        {individual.deduplicationGoldenRecordResults.length ? (
          <DedupeResults
            status={
              deduplicationGoldenRecordDict[
                individual.deduplicationGoldenRecordStatus
              ]
            }
            results={individual.deduplicationGoldenRecordResults}
            individual={individual}
          />
        ) : (
          `${
            deduplicationGoldenRecordDict[
              individual.deduplicationGoldenRecordStatus
            ]
          }`
        )}
      </TableCell>
    </ClickableTableRow>
  );
}
