import { Box } from '@material-ui/core';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { BreadCrumbsItem } from '../../../components/core/BreadCrumbs';
import { FlagTooltip } from '../../../components/core/FlagTooltip';
import { WarningTooltip } from '../../../components/core/WarningTooltip';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { PageHeader } from '../../../components/core/PageHeader';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { IndividualBioData } from '../../../components/population/IndividualBioData/IndividualBioData';
import { IndividualPhotoModal } from '../../../components/population/IndividualPhotoModal';
import { IndividualVulnerabilities } from '../../../components/population/IndividualVulnerabilities/IndividualVunerabilities';
import { hasPermissions, PERMISSIONS } from '../../../config/permissions';
import { usePermissions } from '../../../hooks/usePermissions';
import { isPermissionDeniedError } from '../../../utils/utils';
import {
  IndividualNode,
  useHouseholdChoiceDataQuery,
  useIndividualQuery,
  useAllIndividualsFlexFieldsAttributesQuery,
  useGrievancesChoiceDataQuery,
} from '../../../__generated__/graphql';
import { UniversalActivityLogTable } from '../../tables/UniversalActivityLogTable';
import { useBaseUrl } from '../../../hooks/useBaseUrl';

const Container = styled.div`
  padding: 20px;
  && {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
`;

export const PopulationIndividualsDetailsPage = (): React.ReactElement => {
  const { t } = useTranslation();
  const { id } = useParams();
  const { baseUrl, businessArea } = useBaseUrl();
  const permissions = usePermissions();

  const { data, loading, error } = useIndividualQuery({
    variables: {
      id,
    },
    fetchPolicy: 'cache-and-network',
  });

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useHouseholdChoiceDataQuery();

  const {
    data: flexFieldsData,
    loading: flexFieldsDataLoading,
  } = useAllIndividualsFlexFieldsAttributesQuery();

  const {
    data: grievancesChoices,
    loading: grievancesChoicesLoading,
  } = useGrievancesChoiceDataQuery();

  if (
    loading ||
    choicesLoading ||
    flexFieldsDataLoading ||
    grievancesChoicesLoading
  )
    return <LoadingComponent />;

  if (isPermissionDeniedError(error)) return <PermissionDenied />;

  if (
    !data ||
    !choicesData ||
    !flexFieldsData ||
    !grievancesChoices ||
    permissions === null
  )
    return null;

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Individuals',
      to: `/${baseUrl}/population/individuals`,
    },
  ];

  const getDuplicateTooltip = (individualObject): React.ReactElement => {
    if (individualObject?.status === 'DUPLICATE') {
      return <WarningTooltip confirmed message={t('Confirmed Duplicate')} />;
    }
    if (individualObject?.deduplicationGoldenRecordStatus !== 'UNIQUE') {
      return <WarningTooltip message={t('Possible Duplicate')} />;
    }
    return null;
  };

  const getSanctionListPossibleMatchTooltip = (
    individualObject,
  ): React.ReactElement => {
    if (individualObject?.sanctionListPossibleMatch) {
      return <FlagTooltip message={t('Sanction List Possible Match')} />;
    }
    return null;
  };

  const getSanctionListConfirmedMatchTooltip = (
    individualObject,
  ): React.ReactElement => {
    if (individualObject?.sanctionListConfirmedMatch) {
      return (
        <FlagTooltip message={t('Sanction List Confirmed Match')} confirmed />
      );
    }
    return null;
  };

  const { individual } = data;

  return (
    <>
      <PageHeader
        title={`${t('Individual ID')}: ${individual?.unicefId}`}
        breadCrumbs={
          hasPermissions(
            PERMISSIONS.POPULATION_VIEW_INDIVIDUALS_LIST,
            permissions,
          )
            ? breadCrumbsItems
            : null
        }
        flags={
          <>
            <Box mr={2}>{getDuplicateTooltip(individual)}</Box>
            <Box mr={2}>{getSanctionListPossibleMatchTooltip(individual)}</Box>
            <Box mr={2}>{getSanctionListConfirmedMatchTooltip(individual)}</Box>
          </>
        }
      >
        <Box mr={2}>
          {individual?.photo ? (
            <IndividualPhotoModal individual={individual as IndividualNode} />
          ) : null}
        </Box>
      </PageHeader>

      <Container>
        <IndividualBioData
          baseUrl={baseUrl}
          businessArea={businessArea}
          individual={individual as IndividualNode}
          choicesData={choicesData}
          grievancesChoices={grievancesChoices}
        />
        <IndividualVulnerabilities
          flexFieldsData={flexFieldsData}
          individual={individual as IndividualNode}
        />
        {hasPermissions(PERMISSIONS.ACTIVITY_LOG_VIEW, permissions) && (
          <UniversalActivityLogTable objectId={individual?.id} />
        )}
      </Container>
    </>
  );
};
