import React, { ReactElement } from 'react';
import { useTranslation } from 'react-i18next';
import {
  AllCashPlansAndPaymentPlansQueryVariables,
  CashPlanAndPaymentPlanNode,
  useAllCashPlansAndPaymentPlansQuery,
} from '../../../../__generated__/graphql';
import { useBaseUrl } from '../../../../hooks/useBaseUrl';
import { dateToIsoString } from '../../../../utils/utils';
import { UniversalTable } from '../../UniversalTable';
import { headCells } from './PaymentVerificationHeadCells';
import { PaymentVerificationTableRow } from './PaymentVerificationTableRow';

interface PaymentVerificationTableProps {
  filter?;
  businessArea: string;
  canViewDetails: boolean;
}
export const PaymentVerificationTable = ({
  filter,
  canViewDetails,
  businessArea,
}: PaymentVerificationTableProps): ReactElement => {
  const { t } = useTranslation();
  const { programId } = useBaseUrl();
  const initialVariables: AllCashPlansAndPaymentPlansQueryVariables = {
    businessArea,
    search: filter.search,
    verificationStatus: filter.verificationStatus,
    serviceProvider: filter.serviceProvider,
    deliveryType: filter.deliveryType,
    startDateGte: dateToIsoString(filter.startDate, 'startOfDay'),
    endDateLte: dateToIsoString(filter.endDate, 'endOfDay'),
    program: programId,
  };
  return (
    <UniversalTable<
      CashPlanAndPaymentPlanNode,
      AllCashPlansAndPaymentPlansQueryVariables
    >
      title={t('List of Payment Plans')}
      headCells={headCells}
      query={useAllCashPlansAndPaymentPlansQuery}
      queriedObjectName='allCashPlansAndPaymentPlans'
      initialVariables={initialVariables}
      renderRow={(cashPlanAndPaymentPlanNode) => (
        <PaymentVerificationTableRow
          key={cashPlanAndPaymentPlanNode.id}
          plan={cashPlanAndPaymentPlanNode}
          canViewDetails={canViewDetails}
        />
      )}
    />
  );
};
