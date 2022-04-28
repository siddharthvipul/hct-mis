import { Grid, GridSize, Typography } from '@material-ui/core';
import React from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import {
  decodeIdString,
  grievanceTicketStatusToColor,
  reduceChoices,
  renderUserName,
} from '../../../utils/utils';
import {
  GrievancesChoiceDataQuery,
  GrievanceTicketQuery,
} from '../../../__generated__/graphql';
import { ContainerColumnWithBorder } from '../../core/ContainerColumnWithBorder';
import { ContentLink } from '../../core/ContentLink';
import { LabelizedField } from '../../core/LabelizedField';
import { OverviewContainer } from '../../core/OverviewContainer';
import { StatusBox } from '../../core/StatusBox';
import { Title } from '../../core/Title';
import { UniversalMoment } from '../../core/UniversalMoment';

const StatusContainer = styled.div`
  min-width: 120px;
  max-width: 200px;
`;

interface GrievancesDetailsProps {
  ticket: GrievanceTicketQuery['grievanceTicket'];
  choicesData: GrievancesChoiceDataQuery;
  businessArea: string;
  canViewHouseholdDetails: boolean;
  canViewIndividualDetails: boolean;
}

export function GrievancesDetails({
  ticket,
  choicesData,
  businessArea,
  canViewHouseholdDetails,
  canViewIndividualDetails,
}: GrievancesDetailsProps): React.ReactElement {
  const { t } = useTranslation();
  const statusChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketStatusChoices);

  const categoryChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketCategoryChoices);

  const issueType = ticket.issueType
    ? choicesData.grievanceTicketIssueTypeChoices
        .filter((el) => el.category === ticket.category.toString())[0]
        .subCategories.filter(
          (el) => el.value === ticket.issueType.toString(),
        )[0].name
    : '-';

  return (
    <Grid item xs={12}>
      <ContainerColumnWithBorder>
        <Title>
          <Typography variant='h6'>{t('Details')}</Typography>
        </Title>
        <OverviewContainer>
          <Grid container spacing={6}>
            {[
              {
                label: t('STATUS'),
                value: (
                  <StatusContainer>
                    <StatusBox
                      status={statusChoices[ticket.status]}
                      statusToColor={grievanceTicketStatusToColor}
                    />
                  </StatusContainer>
                ),
                size: 3,
              },
              {
                label: t('CATEGORY'),
                value: <span>{categoryChoices[ticket.category]}</span>,
                size: 3,
              },
              {
                label: t('Issue Type'),
                value: <span>{issueType}</span>,
                size: 6,
              },
              {
                label: t('HOUSEHOLD ID'),
                value: (
                  <span>
                    {ticket.household?.id ? (
                      <ContentLink
                        href={
                          canViewHouseholdDetails
                            ? `/${businessArea}/population/household/${ticket.household.id}`
                            : undefined
                        }
                      >
                        {ticket.household.unicefId}
                      </ContentLink>
                    ) : (
                      '-'
                    )}
                  </span>
                ),
                size: 3,
              },
              {
                label: t('INDIVIDUAL ID'),
                value: (
                  <span>
                    {ticket.individual?.id ? (
                      <ContentLink
                        href={
                          canViewIndividualDetails
                            ? `/${businessArea}/population/individuals/${ticket.individual.id}`
                            : undefined
                        }
                      >
                        {ticket.individual.unicefId}
                      </ContentLink>
                    ) : (
                      '-'
                    )}
                  </span>
                ),
                size: 3,
              },
              {
                label: t('PAYMENT ID'),
                value: (
                  <span>
                    {ticket.paymentRecord?.id ? (
                      <ContentLink
                        href={`/${businessArea}/payment-records/${ticket.paymentRecord.id}`}
                      >
                        {decodeIdString(ticket.paymentRecord.id)}
                      </ContentLink>
                    ) : (
                      '-'
                    )}
                  </span>
                ),
                size: 6,
              },
              {
                label: t('CONSENT'),
                value: <span>{ticket.consent ? 'Yes' : 'No'}</span>,
                size: 3,
              },
              {
                label: t('CREATED BY'),
                value: <span>{renderUserName(ticket.createdBy)}</span>,
                size: 3,
              },
              {
                label: t('DATE CREATED'),
                value: <UniversalMoment>{ticket.createdAt}</UniversalMoment>,
                size: 3,
              },
              {
                label: t('LAST MODIFIED DATE'),
                value: <UniversalMoment>{ticket.updatedAt}</UniversalMoment>,
                size: 3,
              },
              {
                label: t('DESCRIPTION'),
                value: <span>{ticket.description || '-'}</span>,
                size: 6,
              },
              {
                label: t('ASSIGNED TO'),
                value: <span>{renderUserName(ticket.assignedTo) || '-'}</span>,
                size: 6,
              },
              {
                label: t('ADMINISTRATIVE LEVEL 2'),
                value: <span>{ticket.admin}</span>,
                size: 3,
              },
              {
                label: t('AREA / VILLAGE / PAY POINT'),
                value: <span>{ticket.area}</span>,
                size: 3,
              },
              {
                label: t('LANGUAGES SPOKEN'),
                value: <span>{ticket.language || '-'}</span>,
                size: 3,
              },
            ].map((el) => (
              <Grid key={el.label} item xs={el.size as GridSize}>
                <LabelizedField label={el.label}>{el.value}</LabelizedField>
              </Grid>
            ))}
          </Grid>
        </OverviewContainer>
      </ContainerColumnWithBorder>
    </Grid>
  );
}