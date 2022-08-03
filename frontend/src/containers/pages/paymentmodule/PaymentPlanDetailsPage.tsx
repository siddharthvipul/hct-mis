import React from 'react';
import { useParams } from 'react-router-dom';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { AcceptanceProcess } from '../../../components/paymentmodule/PaymentPlanDetails/AcceptanceProcess/AcceptanceProcess';
import { Entitlement } from '../../../components/paymentmodule/PaymentPlanDetails/Entitlement/Entitlement';
import { FspSection } from '../../../components/paymentmodule/PaymentPlanDetails/FspSection';
import { PaymentPlanDetails } from '../../../components/paymentmodule/PaymentPlanDetails/PaymentPlanDetails';
import { PaymentPlanDetailsHeader } from '../../../components/paymentmodule/PaymentPlanDetails/PaymentPlanDetailsHeader';
import { PaymentPlanDetailsResults } from '../../../components/paymentmodule/PaymentPlanDetails/PaymentPlanDetailsResults';
import { hasPermissions, PERMISSIONS } from '../../../config/permissions';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { usePermissions } from '../../../hooks/usePermissions';
import { PaymentsTable } from '../../tables/paymentmodule/PaymentsTable';
import { usePaymentPlanQuery } from '../../../__generated__/graphql';
import { LoadingComponent } from '../../../components/core/LoadingComponent';

export const PaymentPlanDetailsPage = (): React.ReactElement => {
  const { id } = useParams();
  const permissions = usePermissions();
  const businessArea = useBusinessArea();
  const { data, loading } = usePaymentPlanQuery({
    variables: { id },
    fetchPolicy: 'cache-and-network',
  });

  if (permissions === null) return null;
  if (!data) return null;
  if (loading) return <LoadingComponent />;
  if (!hasPermissions(PERMISSIONS.PAYMENT_MODULE_VIEW_DETAILS, permissions))
    return <PermissionDenied />;

  return (
    <>
      <PaymentPlanDetailsHeader
        paymentPlan={data.paymentPlan}
        businessArea={businessArea}
        permissions={permissions}
      />
      <PaymentPlanDetails
        businessArea={businessArea}
        permissions={permissions}
        paymentPlan={data.paymentPlan}
      />
      <AcceptanceProcess
        businessArea={businessArea}
        permissions={permissions}
      />
      <Entitlement businessArea={businessArea} permissions={permissions} />
      <FspSection businessArea={businessArea} permissions={permissions} />
      <PaymentPlanDetailsResults paymentPlan={data.paymentPlan} />
      <PaymentsTable businessArea={businessArea} filter={{paymentPlanId: id}} />
    </>
  );
};
