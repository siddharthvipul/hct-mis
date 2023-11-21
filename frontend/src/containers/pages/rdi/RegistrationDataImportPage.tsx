import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import { PageHeader } from '../../../components/core/PageHeader';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { RegistrationDataImportCreateDialog } from '../../../components/rdi/create/RegistrationDataImportCreateDialog';
import { RegistrationFilters } from '../../../components/rdi/RegistrationFilters';
import { hasPermissions, PERMISSIONS } from '../../../config/permissions';
import { usePermissions } from '../../../hooks/usePermissions';
import { getFilterFromQueryParams } from '../../../utils/utils';
import { RegistrationDataImportTable } from '../../tables/rdi/RegistrationDataImportTable';
import { useProgramQuery } from "../../../__generated__/graphql";
import {useBaseUrl} from "../../../hooks/useBaseUrl";

const initialFilter = {
  search: '',
  importedBy: '',
  status: '',
  sizeMin: '',
  sizeMax: '',
  importDateRangeMin: '',
  importDateRangeMax: '',
};

export const RegistrationDataImportPage = (): React.ReactElement => {
  const location = useLocation();
  const { programId } = useBaseUrl();
  const permissions = usePermissions();
  const { t } = useTranslation();

  const [filter, setFilter] = useState(
    getFilterFromQueryParams(location, initialFilter),
  );
  const [appliedFilter, setAppliedFilter] = useState(
    getFilterFromQueryParams(location, initialFilter),
  );

  const { data, loading: programLoading } = useProgramQuery({
    variables: { id: programId },
    fetchPolicy: 'cache-and-network',
  });

  if (permissions === null || programLoading) return null;

  let isImportDisabled = false;
  if (data.program && data.program.status !== "ACTIVE") {
    isImportDisabled = true
  }

  if (!hasPermissions(PERMISSIONS.RDI_VIEW_LIST, permissions))
    return <PermissionDenied />;

  const toolbar = (
    <PageHeader title={t('Registration Data Import')}>
      {hasPermissions(PERMISSIONS.RDI_IMPORT_DATA, permissions) && (
        <RegistrationDataImportCreateDialog isImportDisabled={isImportDisabled} />
      )}
    </PageHeader>
  );
  return (
    <div>
      {toolbar}
      <RegistrationFilters
        filter={filter}
        setFilter={setFilter}
        initialFilter={initialFilter}
        appliedFilter={appliedFilter}
        setAppliedFilter={setAppliedFilter}
      />
      <RegistrationDataImportTable
        filter={appliedFilter}
        canViewDetails={hasPermissions(
          PERMISSIONS.RDI_VIEW_DETAILS,
          permissions,
        )}
      />
    </div>
  );
};
