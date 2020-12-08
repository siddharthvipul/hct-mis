import React from 'react';
import styled from 'styled-components';
import { useParams } from 'react-router-dom';
import { PageHeader } from '../../components/PageHeader';
import { BreadCrumbsItem } from '../../components/BreadCrumbs';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { IndividualsBioData } from '../../components/population/IndividualBioData';
import {
  IndividualNode,
  useIndividualQuery,
} from '../../__generated__/graphql';
import { IndividualVulnerabilities } from '../../components/population/IndividualVunerabilities';
import { CashPlus } from '../../components/population/CashPlus';
import { UniversalActivityLogTable } from '../tables/UniversalActivityLogTable';
import { PermissionDenied } from '../../components/PermissionDenied';
import { hasPermissions, PERMISSIONS } from '../../config/permissions';
import { usePermissions } from '../../hooks/usePermissions';

const Container = styled.div`
  padding: 20px;
  && {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
`;

export function PopulationIndividualsDetailsPage(): React.ReactElement {
  const { id } = useParams();
  const businessArea = useBusinessArea();
  const permissions = usePermissions();

  const { data, loading } = useIndividualQuery({
    variables: {
      id,
    },
  });

  if (loading || permissions === null) return null;

  if (
    !hasPermissions(
      PERMISSIONS.POPULATION_VIEW_INDIVIDUALS_DETAILS,
      permissions,
    )
  ) {
    return <PermissionDenied />;
  }

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Individuals',
      to: `/${businessArea}/population/individuals`,
    },
  ];

  const { individual } = data;
  return (
    <div>
      <PageHeader
        title={`Individual ID: ${individual.unicefId}`}
        breadCrumbs={breadCrumbsItems}
        withFlag={individual.sanctionListPossibleMatch}
        withTriangle={individual.deduplicationGoldenRecordStatus !== 'UNIQUE'}
      />
      <Container>
        <IndividualsBioData individual={individual as IndividualNode} />
        <IndividualVulnerabilities individual={individual as IndividualNode} />
        <CashPlus individual={individual as IndividualNode} />
        <UniversalActivityLogTable objectId={individual.id} />
      </Container>
    </div>
  );
}
