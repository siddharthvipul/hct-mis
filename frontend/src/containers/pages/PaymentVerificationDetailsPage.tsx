import React, { useState } from 'react';
import styled from 'styled-components';
import { Button, Grid, Typography, Box } from '@material-ui/core';
import { Doughnut } from 'react-chartjs-2';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Moment from 'react-moment';
import { PageHeader } from '../../components/PageHeader';
import { LabelizedField } from '../../components/LabelizedField';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { BreadCrumbsItem } from '../../components/BreadCrumbs';
import { NewPaymentVerificationDialog } from '../../components/payments/NewPaymentVerificationDialog';
import { UniversalActivityLogTable } from '../tables/UniversalActivityLogTable';
import { EditNewPaymentVerificationDialog } from '../../components/payments/EditNewPaymentVerificationDialog';
import { ActivateVerificationPlan } from '../../components/payments/ActivateVerificationPlan';
import { FinishVerificationPlan } from '../../components/payments/FinishVerificationPlan';
import { DiscardVerificationPlan } from '../../components/payments/DiscardVerificationPlan';
import { useCashPlanQuery } from '../../__generated__/graphql';
import { LoadingComponent } from '../../components/LoadingComponent';
import {
  decodeIdString,
  paymentVerificationStatusToColor,
} from '../../utils/utils';
import { StatusBox } from '../../components/StatusBox';
import { VerificationRecordsTable } from '../tables/VerificationRecordsTable';
import { Missing } from '../../components/Missing';
import { useDebounce } from '../../hooks/useDebounce';
import { VerificationRecordsFilters } from '../tables/VerificationRecordsTable/VerificationRecordsFilters';

const Container = styled.div`
  display: flex;
  flex: 1;
  width: 100%;
  background-color: #fff;
  padding: ${({ theme }) => theme.spacing(8)}px
    ${({ theme }) => theme.spacing(11)}px;
  flex-direction: column;
  border-color: #b1b1b5;
  border-bottom-width: 1px;
  border-bottom-style: solid;
`;

const Title = styled.div`
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;

const ChartContainer = styled.div`
  width: 100px;
  height: 100px;
`;

const BorderLeftBox = styled.div`
  padding-left: ${({ theme }) => theme.spacing(6)}px;
  border-left: 1px solid #e0e0e0;
  height: 100%;
`;

const BottomTitle = styled.div`
  color: rgba(0, 0, 0, 0.38);
  font-size: 24px;
  line-height: 28px;
  text-align: center;
  padding: 70px;
`;

const TableWrapper = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 20px;
  padding-bottom: 0;
`;
const StatusContainer = styled.div`
  min-width: 120px;
  max-width: 200px;
`;
// interface PaymentVerificationDetailsProps {
//   registration: 'registr';
// }

export function PaymentVerificationDetailsPage(): React.ReactElement {
  const { t } = useTranslation();
  const businessArea = useBusinessArea();
  const [filter, setFilter] = useState({
    search: null,
  });
  const debouncedFilter = useDebounce(filter, 500);
  const { id } = useParams();
  const { data, loading } = useCashPlanQuery({
    variables: { id },
  });
  if (loading) {
    return <LoadingComponent />;
  }
  if (!data) {
    return null;
  }

  const { cashPlan } = data;
  const verificationPlan =
    cashPlan && cashPlan.verifications && cashPlan.verifications.edges.length
      ? cashPlan.verifications.edges[0].node
      : null;
  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Payment Verification',
      to: `/${businessArea}/payment-verification/`,
    },
  ];

  const toolbar = (
    <PageHeader
      title={`Cash Plan ${decodeIdString(cashPlan.id)}`}
      breadCrumbs={breadCrumbsItems}
    >
      <>
        {cashPlan.verificationStatus === 'PENDING' &&
          cashPlan.verifications &&
          cashPlan.verifications.edges.length === 0 && (
            <NewPaymentVerificationDialog cashPlanId={cashPlan.id} />
          )}
        {cashPlan.verificationStatus === 'PENDING' &&
          cashPlan.verifications &&
          cashPlan.verifications.edges.length !== 0 && (
            <Box display='flex'>
              <EditNewPaymentVerificationDialog /> <ActivateVerificationPlan />
            </Box>
          )}
        {cashPlan.verificationStatus === 'ACTIVE' &&
          cashPlan.verifications &&
          cashPlan.verifications.edges.length !== 0 && (
            <Box display='flex'>
              <FinishVerificationPlan />
              <DiscardVerificationPlan />
            </Box>
          )}
      </>
    </PageHeader>
  );

  return (
    <>
      {toolbar}
      <Container>
        <Grid container>
          <Grid item xs={9}>
            <Title>
              <Typography variant='h6'>Cash Plan Details</Typography>
            </Title>
            <Grid container>
              <Grid item xs={4}>
                <LabelizedField label='PROGRAMME NAME'>
                  <p>{cashPlan.program.name}</p>
                </LabelizedField>
              </Grid>
              <Grid item xs={4}>
                <LabelizedField label='PROGRAMME ID'>
                  <p>{decodeIdString(cashPlan.program.id)}</p>
                </LabelizedField>
              </Grid>
              <Grid item xs={4}>
                <LabelizedField label='PAYMENT RECORDS'>
                  <p>{cashPlan.paymentRecords.totalCount}</p>
                </LabelizedField>
              </Grid>
              <Grid item xs={4}>
                <LabelizedField label='START DATE'>
                  <p>
                    <Moment format='DD/MM/YYYY'>{cashPlan.startDate}</Moment>
                  </p>
                </LabelizedField>
              </Grid>
              <Grid item xs={4}>
                <LabelizedField label='END DATE'>
                  <p>
                    <Moment format='DD/MM/YYYY'>{cashPlan.endDate}</Moment>
                  </p>
                </LabelizedField>
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={3}>
            <BorderLeftBox>
              <Title>
                <Typography variant='h6'>
                  Bank reconciliation <Missing />
                </Typography>
              </Title>
              <Grid container>
                <Grid item xs={6}>
                  <Grid container direction='column'>
                    <LabelizedField label='SUCCESSFUL'>
                      <p>90%</p>
                    </LabelizedField>
                    <LabelizedField label='ERRONEUS'>
                      <p>10%</p>
                    </LabelizedField>
                  </Grid>
                </Grid>
                <Grid item xs={6}>
                  <ChartContainer>
                    <Doughnut
                      width={100}
                      height={100}
                      options={{
                        maintainAspectRatio: false,
                        cutoutPercentage: 65,
                        legend: {
                          display: false,
                        },
                      }}
                      data={{
                        labels: ['Successful', 'Erroneus'],
                        datasets: [
                          {
                            data: [90, 10],
                            backgroundColor: ['#00509F', '#FFAA1F'],
                            hoverBackgroundColor: ['#00509F', '#FFAA1F'],
                          },
                        ],
                      }}
                    />
                  </ChartContainer>
                </Grid>
              </Grid>
            </BorderLeftBox>
          </Grid>
        </Grid>
      </Container>
      {cashPlan.verifications && cashPlan.verifications.edges.length ? (
        <Container>
          <Title>
            <Typography variant='h6'>Verification Plan Details</Typography>
          </Title>
          <Grid container>
            <Grid item xs={9}>
              <Grid container>
                <Grid item xs={4}>
                  <LabelizedField label='STATUS'>
                    <StatusContainer>
                      <StatusBox
                        status={verificationPlan.status}
                        statusToColor={paymentVerificationStatusToColor}
                      />
                    </StatusContainer>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='SAMPLE SIZE'>
                    <p>{verificationPlan.sampleSize}</p>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='RECEIVED'>
                    <p>{verificationPlan.receivedCount}</p>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='VERIFICATION METHOD'>
                    <p>{verificationPlan.verificationMethod}</p>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='RESPONDED'>
                    <p>{verificationPlan.respondedCount}</p>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='NOT RECEIVED'>
                    <p>{verificationPlan.notReceivedCount}</p>
                  </LabelizedField>
                </Grid>
                <Grid item xs={4}>
                  <LabelizedField label='SAMPLING'>
                    <p>{verificationPlan.sampling}</p>
                  </LabelizedField>
                </Grid>
              </Grid>
            </Grid>
            <Grid item xs={3}>
              <Grid container>
                <Grid item xs={6}>
                  <Grid container direction='column'>
                    <LabelizedField label='RECEIVED CORRECT AMOUNT'>
                      <p>{verificationPlan.receivedCount}</p>
                    </LabelizedField>
                    <LabelizedField label='RECEIVED WRONG AMOUNT'>
                      <p>{verificationPlan.receivedWithProblemsCount}</p>
                    </LabelizedField>
                  </Grid>
                </Grid>
                <Grid item xs={6}>
                  <ChartContainer>
                    <Doughnut
                      width={100}
                      height={100}
                      options={{
                        maintainAspectRatio: false,
                        cutoutPercentage: 65,
                        legend: {
                          display: false,
                        },
                      }}
                      data={{
                        labels: ['CORRECT', 'WRONG'],
                        datasets: [
                          {
                            data: [
                              verificationPlan.receivedCount,
                              verificationPlan.receivedWithProblemsCount,
                            ],
                            backgroundColor: ['#74C304', '#DADADA'],
                            hoverBackgroundColor: ['#74C304', '#DADADA'],
                          },
                        ],
                      }}
                    />
                  </ChartContainer>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Container>
      ) : null}
      {cashPlan.verifications && cashPlan.verifications.edges.length ? (
        <>
          <Container>
            <VerificationRecordsFilters
              filter={filter}
              onFilterChange={setFilter}
            />
          </Container>
          <Container>
            <VerificationRecordsTable
              filter={debouncedFilter}
              id={verificationPlan.id}
            />
          </Container>
        </>
      ) : null}
      {!cashPlan.verifications && cashPlan.verifications.edges.length && (
        <BottomTitle>
          To see more details please create Verification Plan
        </BottomTitle>
      )}
      <TableWrapper>
        <UniversalActivityLogTable objectId='some id' />
      </TableWrapper>
    </>
    //connect it later
  );
}
