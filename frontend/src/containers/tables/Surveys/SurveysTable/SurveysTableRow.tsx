import TableCell from '@mui/material/TableCell';
import React from 'react';
import { useHistory } from 'react-router-dom';
import { BlackLink } from '../../../../components/core/BlackLink';
import { ClickableTableRow } from '../../../../components/core/Table/ClickableTableRow';
import { UniversalMoment } from '../../../../components/core/UniversalMoment';
import { renderUserName } from '../../../../utils/utils';
import { SurveyNode } from '../../../../__generated__/graphql';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';

interface SurveysTableRowProps {
  survey: SurveyNode;
  canViewDetails: boolean;
  categoryDict;
}

export const SurveysTableRow = ({
  survey,
  canViewDetails,
  categoryDict,
}: SurveysTableRowProps): React.ReactElement => {
  const history = useHistory();
  const { baseUrl } = useBaseUrl();
  const surveyDetailsPath = `/${baseUrl}/accountability/surveys/${survey.id}`;

  const handleClick = (): void => {
    history.push(surveyDetailsPath);
  };
  return (
    <ClickableTableRow
      hover
      onClick={canViewDetails ? handleClick : undefined}
      role="checkbox"
      key={survey.unicefId}
    >
      <TableCell align="left">
        {canViewDetails ? (
          <BlackLink to={surveyDetailsPath}>{survey.unicefId}</BlackLink>
        ) : (
          survey.unicefId
        )}
      </TableCell>
      <TableCell align="left">{survey.title}</TableCell>
      <TableCell align="left">{categoryDict[survey.category]}</TableCell>
      <TableCell align="left">{survey.numberOfRecipients}</TableCell>
      <TableCell align="left">{renderUserName(survey.createdBy)}</TableCell>
      <TableCell align="left">
        <UniversalMoment>{survey.createdAt}</UniversalMoment>
      </TableCell>
    </ClickableTableRow>
  );
};
