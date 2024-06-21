import { Box, Typography } from '@mui/material';
import * as React from 'react';
import { useTranslation } from 'react-i18next';
import { AllChartsQuery } from '@generated/graphql';
import { PaymentVerificationChart } from '../../charts/PaymentVerificationChart';
import { DashboardPaper } from '../../DashboardPaper';

interface PaymentVerificationSectionProps {
  data: AllChartsQuery['chartPaymentVerification'];
}
export function PaymentVerificationSection({
  data,
}: PaymentVerificationSectionProps): React.ReactElement {
  const { t } = useTranslation();
  if (!data) return null;

  const renderContacted = () => {
    return data.households === 1
      ? t('Household contacted')
      : t('Households contacted');
  };

  return (
    <DashboardPaper title={t('Payment Verification')}>
      <Box mt={3}>
        <Typography variant="subtitle2">
          {data.households} {renderContacted()}
        </Typography>
        <Typography variant="caption">
          {(data.averageSampleSize * 100).toFixed(0)}%{t('average sampling')}
        </Typography>
      </Box>
      {data.datasets && <PaymentVerificationChart data={data.datasets} />}
    </DashboardPaper>
  );
}
