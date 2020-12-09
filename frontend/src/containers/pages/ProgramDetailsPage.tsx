import React from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { ProgramDetails } from '../../components/programs/ProgramDetails';
import { CashPlanTable } from '../tables/CashPlanTable';
import {
  ProgramNode,
  ProgramStatus,
  useProgrammeChoiceDataQuery,
  useProgramQuery,
} from '../../__generated__/graphql';
import { LoadingComponent } from '../../components/LoadingComponent';
import { UniversalActivityLogTable } from '../tables/UniversalActivityLogTable';
import { ProgramDetailsPageHeader } from './headers/ProgramDetailsPageHeader';
import { usePermissions } from '../../hooks/usePermissions';
import { hasPermissions, PERMISSIONS } from '../../config/permissions';
import { PermissionDenied } from '../../components/PermissionDenied';

const Container = styled.div`
  && {
    display: flex;
    flex-direction: column;
    min-width: 100%;
  }
`;

const TableWrapper = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 20px;
  padding-bottom: 0;
`;

const NoCashPlansContainer = styled.div`
  margin-top: ${({ theme }) => theme.spacing(30)}px;
`;
const NoCashPlansTitle = styled.div`
  color: rgba(0, 0, 0, 0.38);
  font-size: 24px;
  line-height: 28px;
  text-align: center;
`;
const NoCashPlansSubTitle = styled.div`
  color: rgba(0, 0, 0, 0.38);
  font-size: 16px;
  line-height: 19px;
  text-align: center;
`;

export function ProgramDetailsPage(): React.ReactElement {
  const { id } = useParams();
  const { data, loading } = useProgramQuery({
    variables: { id },
  });
  const {
    data: choices,
    loading: choicesLoading,
  } = useProgrammeChoiceDataQuery();
  const permissions = usePermissions();

  if (loading || choicesLoading) return <LoadingComponent />;

  if (permissions === null) return null;

  if (
    !hasPermissions(PERMISSIONS.PRORGRAMME_VIEW_LIST_AND_DETAILS, permissions)
  )
    return <PermissionDenied />;

  if (!data || !choices) return null;

  const program = data.program as ProgramNode;
  return (
    <div>
      <ProgramDetailsPageHeader
        program={program}
        canActivate={hasPermissions(
          PERMISSIONS.PROGRAMME_ACTIVATE,
          permissions,
        )}
        canEdit={hasPermissions(PERMISSIONS.PROGRAMME_UPDATE, permissions)}
        canRemove={hasPermissions(PERMISSIONS.PROGRAMME_REMOVE, permissions)}
        canFinish={hasPermissions(PERMISSIONS.PROGRAMME_FINISH, permissions)}
      />
      <Container>
        <ProgramDetails program={program} choices={choices} />
        {program.status === ProgramStatus.Draft ? (
          <NoCashPlansContainer>
            <NoCashPlansTitle>
              To see more details please Activate your Programme
            </NoCashPlansTitle>
            <NoCashPlansSubTitle>
              All data will be pushed to CashAssist. You can edit this plan even
              if it is active.
            </NoCashPlansSubTitle>
          </NoCashPlansContainer>
        ) : (
          <TableWrapper>
            <CashPlanTable program={program} />
          </TableWrapper>
        )}
        <TableWrapper>
          <UniversalActivityLogTable objectId={program.id} />
        </TableWrapper>
      </Container>
    </div>
  );
}
