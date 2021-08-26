import { Box, Paper, Typography } from '@material-ui/core';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { GRIEVANCE_TICKET_STATES } from '../../utils/constants';
import { decodeIdString } from '../../utils/utils';
import { useExistingGrievanceTicketsQuery } from '../../__generated__/graphql';
import { ContentLink } from '../ContentLink';
import { LabelizedField } from '../LabelizedField';
import { LoadingComponent } from '../LoadingComponent';

const StyledBox = styled(Paper)`
  border-radius: 3px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 26px 22px;
`;
const Title = styled.div`
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;

const BlueBold = styled.div`
  color: ${({ theme }) => theme.hctPalette.navyBlue};
  font-weight: 500;
  cursor: pointer;
`;

export function OtherRelatedTicketsCreate({ values }): React.ReactElement {
  const { t } = useTranslation();
  const businessArea = useBusinessArea();
  const [show, setShow] = useState(false);

  const { data, loading } = useExistingGrievanceTicketsQuery({
    variables: {
      businessArea,
      household:
        //TODO Janek to jeszcze kiedyś wymyśli
        decodeIdString(values?.selectedHousehold?.id) ||
        '294cfa7e-b16f-4331-8014-a22ffb2b8b3c',
      //adding some random ID to get 0 results if there is no household id.
    },
  });
  if (loading) return <LoadingComponent />;
  if (!data) return null;

  const householdTickets = data.existingGrievanceTickets.edges;
  const renderIds = (tickets): React.ReactElement =>
    tickets.length
      ? tickets.map((edge) => (
          <Box key={edge.node.id} mb={1}>
            <ContentLink
              href={`/${businessArea}/grievance-and-feedback/${edge.node.id}`}
            >
              {edge.node.unicefId}
            </ContentLink>
          </Box>
        ))
      : '-';

  const openHouseholdTickets = householdTickets.length
    ? householdTickets.filter(
        (edge) => edge.node.status !== GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];
  const closedHouseholdTickets = householdTickets.length
    ? householdTickets.filter(
        (edge) => edge.node.status === GRIEVANCE_TICKET_STATES.CLOSED,
      )
    : [];

  return householdTickets.length ? (
    <StyledBox>
      <Title>
        <Typography variant='h6'>{t('Other Related Tickets')}</Typography>
      </Title>
      <Box display='flex' flexDirection='column'>
        <LabelizedField
          label={`${t('For Household')} ${values?.selectedHousehold?.unicefId ||
            '-'} `}
        >
          <>{renderIds(openHouseholdTickets)}</>
        </LabelizedField>
        {!show && closedHouseholdTickets.length ? (
          <Box mt={3}>
            <BlueBold onClick={() => setShow(true)}>
              {t('SHOW CLOSED TICKETS')} ({closedHouseholdTickets.length})
            </BlueBold>
          </Box>
        ) : null}
        {show && (
          <Box mb={3} mt={3}>
            <Typography>{t('Closed Tickets')}</Typography>
            <LabelizedField
              label={`${t('For Household')} ${values?.selectedHousehold
                ?.unicefId || '-'} `}
            >
              <>{renderIds(closedHouseholdTickets)}</>
            </LabelizedField>
          </Box>
        )}
        {show && closedHouseholdTickets.length ? (
          <BlueBold onClick={() => setShow(false)}>
            {t('HIDE CLOSED TICKETS')} ({closedHouseholdTickets.length})
          </BlueBold>
        ) : null}
      </Box>
    </StyledBox>
  ) : null;
}
