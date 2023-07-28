import React, { ReactElement } from 'react';
import { useTranslation } from 'react-i18next';
import {
  AllSurveysQueryVariables,
  SurveyNode,
  SurveysChoiceDataQuery,
  useAllSurveysQuery,
} from '../../../../__generated__/graphql';
import { TableWrapper } from '../../../../components/core/TableWrapper';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';
import { choicesToDict, decodeIdString } from '../../../../utils/utils';
import { UniversalTable } from '../../UniversalTable';
import { headCells } from './SurveysTableHeadCells';
import { SurveysTableRow } from './SurveysTableRow';

interface SurveysTableProps {
  filter;
  canViewDetails: boolean;
  choicesData: SurveysChoiceDataQuery;
}

export const SurveysTable = ({
  filter,
  canViewDetails,
  choicesData,
}: SurveysTableProps): ReactElement => {
  const { programId } = useBaseUrl();
  const { t } = useTranslation();
  const initialVariables: AllSurveysQueryVariables = {
    search: filter.search,
    targetPopulation: filter.targetPopulation || '',
    createdBy: decodeIdString(filter.createdBy) || '',
    createdAtRange: filter.createdAtRange
      ? JSON.stringify(filter.createdAtRange)
      : '',
    program: programId,
  };
  const categoryDict = choicesToDict(choicesData.surveyCategoryChoices);

  return (
    <TableWrapper>
      <UniversalTable<SurveyNode, AllSurveysQueryVariables>
        headCells={headCells}
        title={t('Surveys List')}
        rowsPerPageOptions={[10, 15, 20]}
        query={useAllSurveysQuery}
        queriedObjectName='allSurveys'
        defaultOrderBy='createdAt'
        defaultOrderDirection='desc'
        initialVariables={initialVariables}
        renderRow={(row) => (
          <SurveysTableRow
            key={row.id}
            survey={row}
            canViewDetails={canViewDetails}
            categoryDict={categoryDict}
          />
        )}
      />
    </TableWrapper>
  );
};
