import React from 'react';
import TableCell from '@material-ui/core/TableCell';
import { Radio } from '@material-ui/core';
import { Link } from 'react-router-dom';
import { AllIndividualsQuery } from '../../../__generated__/graphql';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { sexToCapitalize } from '../../../utils/utils';
import { ClickableTableRow } from '../../table/ClickableTableRow';
import { UniversalMoment } from '../../UniversalMoment';

interface LookUpIndividualTableRowProps {
  individual: AllIndividualsQuery['allIndividuals']['edges'][number]['node'];
  radioChangeHandler: (
    individual: AllIndividualsQuery['allIndividuals']['edges'][number]['node'],
  ) => void;
  selectedIndividual: AllIndividualsQuery['allIndividuals']['edges'][number]['node'];
}

export function LookUpIndividualTableRow({
  individual,
  radioChangeHandler,
  selectedIndividual,
}: LookUpIndividualTableRowProps): React.ReactElement {
  const businessArea = useBusinessArea();
  const renderPrograms = (): string => {
    const programNames = individual?.household?.programs?.edges?.map(
      (edge) => edge.node.name,
    );
    return programNames?.length ? programNames.join(', ') : '-';
  };
  return (
    <ClickableTableRow hover role='checkbox' key={individual.id}>
      <TableCell padding='checkbox'>
        <Radio
          color='primary'
          checked={selectedIndividual?.id === individual.id}
          onChange={() => {
            radioChangeHandler(individual);
          }}
          value={individual.id}
          name='radio-button-household'
          inputProps={{ 'aria-label': individual.id }}
        />
      </TableCell>
      <TableCell align='left'>
        <Link
          target='_blank'
          rel='noopener noreferrer'
          to={`/${businessArea}/population/individuals/${individual.id}`}
        >
          {individual.unicefId}
        </Link>
      </TableCell>
      <TableCell align='left'>{individual.fullName}</TableCell>
      <TableCell align='left'>
        {individual.household ? individual.household.unicefId : ''}
      </TableCell>
      <TableCell align='right'>{individual.age}</TableCell>
      <TableCell align='left'>{sexToCapitalize(individual.sex)}</TableCell>
      <TableCell align='left'>
        {individual?.household?.admin2?.title || '-'}
      </TableCell>
      <TableCell align='left'>{renderPrograms()}</TableCell>
      <TableCell align='left'>
        <UniversalMoment>{individual.lastRegistrationDate}</UniversalMoment>
      </TableCell>
    </ClickableTableRow>
  );
}
