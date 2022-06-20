import { Button, Grid, Typography } from '@material-ui/core';
import { GetApp } from '@material-ui/icons';
import CheckIcon from '@material-ui/icons/Check';
import EmailIcon from '@material-ui/icons/Email';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { BreadCrumbsItem } from '../../../components/core/BreadCrumbs';
import { ContainerColumnWithBorder } from '../../../components/core/ContainerColumnWithBorder';
import { LabelizedField } from '../../../components/core/LabelizedField';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { OverviewContainer } from '../../../components/core/OverviewContainer';
import { PageHeader } from '../../../components/core/PageHeader';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { StatusBox } from '../../../components/core/StatusBox';
import { Title } from '../../../components/core/Title';
import { UniversalMoment } from '../../../components/core/UniversalMoment';
import { hasPermissions, PERMISSIONS } from '../../../config/permissions';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { usePermissions } from '../../../hooks/usePermissions';
import { reduceChoices, reportStatusToColor } from '../../../utils/utils';
import {
  useReportChoiceDataQuery,
  useReportQuery,
} from '../../../__generated__/graphql';

const IconContainer = styled.div`
  color: #d1d1d1;
  font-size: 90px;
`;
const GreyText = styled.div`
  color: #abacae;
  font-size: 24px;
  text-align: center;
`;

const IconsContainer = styled.div`
  margin-top: 120px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 50px;
`;
export const ReportingDetailsPage = (): React.ReactElement => {
  const { t } = useTranslation();
  const { id } = useParams();
  const businessArea = useBusinessArea();
  const permissions = usePermissions();

  const { data, loading } = useReportQuery({
    variables: { id },
  });
  const {
    data: choicesData,
    loading: choicesLoading,
  } = useReportChoiceDataQuery();

  if (loading || choicesLoading) return <LoadingComponent />;
  if (permissions === null) return null;
  if (!hasPermissions(PERMISSIONS.REPORTING_EXPORT, permissions))
    return <PermissionDenied />;

  if (!data || !choicesData) return null;
  const { report } = data;

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: t('Reporting'),
      to: `/${businessArea}/reporting/`,
    },
  ];

  const statusChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.reportStatusChoices);

  const typeChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.reportTypesChoices);

  const FieldsArray: {
    label: string;
    value: React.ReactElement | string;
    size: boolean | 3 | 6 | 8 | 11 | 'auto' | 1 | 2 | 4 | 5 | 7 | 9 | 10 | 12;
  }[] = [
    {
      label: t('STATUS'),
      value: (
        <StatusBox
          status={statusChoices[report.status]}
          statusToColor={reportStatusToColor}
        />
      ),
      size: 3,
    },
    {
      label: t('Report Type'),
      value: typeChoices[report.reportType],
      size: 3,
    },
    {
      label: t('Timeframe'),
      value: (
        <span>
          <UniversalMoment>{report.dateFrom}</UniversalMoment> -{' '}
          <UniversalMoment>{report.dateTo}</UniversalMoment>
        </span>
      ),
      size: 3,
    },
    {
      label: t('Creation Date'),
      value: <UniversalMoment>{report.createdAt}</UniversalMoment>,
      size: 3,
    },
    {
      label: t('Created By'),
      value: (
        <span>
          {report.createdBy.firstName} {report.createdBy.lastName}
        </span>
      ),
      size: 3,
    },
    {
      label: t('Programme'),
      value: report.program?.name,
      size: 3,
    },
    {
      label: t('Administrative Level 2'),
      value: (
        <span>
          {report.adminArea?.edges.map((edge) => edge.node.name).join(', ') ||
            '-'}
        </span>
      ),
      size: 3,
    },
  ];
  return (
    <>
      <PageHeader
        title={
          <span>
            {typeChoices[report.reportType]}{' '}
            <UniversalMoment>{report.createdAt}</UniversalMoment>
          </span>
        }
        breadCrumbs={breadCrumbsItems}
      >
        {report.fileUrl ? (
          <Button
            color='primary'
            variant='contained'
            startIcon={<GetApp />}
            href={report.fileUrl}
          >
            {t('DOWNLOAD REPORT')}
          </Button>
        ) : null}
      </PageHeader>
      <ContainerColumnWithBorder>
        <Title>
          <Typography variant='h6'>{t('Details')}</Typography>
        </Title>
        <OverviewContainer>
          <Grid container spacing={6}>
            {FieldsArray.map((el) => (
              <Grid key={el.label} item xs={el.size}>
                <LabelizedField label={el.label}>{el.value}</LabelizedField>
              </Grid>
            ))}
          </Grid>
        </OverviewContainer>
      </ContainerColumnWithBorder>
      {report.status === 2 && (
        <>
          <IconsContainer>
            <IconContainer>
              <EmailIcon fontSize='inherit' />
            </IconContainer>
            <IconContainer>
              <CheckIcon fontSize='inherit' />
            </IconContainer>
          </IconsContainer>
          <GreyText>
            {t(
              'Report was successfully generated and sent to email address of the creator.',
            )}
          </GreyText>
        </>
      )}
    </>
  );
};
