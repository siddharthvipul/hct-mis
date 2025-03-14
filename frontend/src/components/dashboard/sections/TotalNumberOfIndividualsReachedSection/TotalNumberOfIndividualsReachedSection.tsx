import { Box, Button, DialogContent, Grid } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import * as React from 'react';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { Dialog } from '@containers/dialogs/Dialog';
import { DialogActions } from '@containers/dialogs/DialogActions';
import { DialogContainer } from '@containers/dialogs/DialogContainer';
import { DialogFooter } from '@containers/dialogs/DialogFooter';
import { formatNumber } from '@utils/utils';
import { AllChartsQuery } from '@generated/graphql';
import { IndividualsReachedByAgeAndGenderGroupsChart } from '../../charts/IndividualsReachedByAgeAndGenderGroupsChart';
import { IndividualsWithDisabilityReachedByAgeGroupsChart } from '../../charts/IndividualsWithDisabilityReachedByAgeGroupsChart';
import {
  CardAmountLink,
  CardTitle,
  DashboardCard,
  IconContainer,
} from '../../DashboardCard';

const ChartWrapper = styled.div`
  height: 200px;
`;
const Title = styled(Box)`
  font-size: 18px;
  font-weight: normal;
`;
interface TotalNumberOfIndividualsReachedSectionProps {
  data: AllChartsQuery['sectionIndividualsReached'];
  chartDataIndividuals: AllChartsQuery['chartIndividualsReachedByAgeAndGender'];
  chartDataIndividualsDisability: AllChartsQuery['chartIndividualsWithDisabilityReachedByAge'];
}

export function TotalNumberOfIndividualsReachedSection({
  data,
  chartDataIndividuals,
  chartDataIndividualsDisability,
}: TotalNumberOfIndividualsReachedSectionProps): React.ReactElement {
  const [dialogOpen, setDialogOpen] = useState(false);
  const { t } = useTranslation();
  if (!data) return null;

  return (
    <>
      <DashboardCard color="#345DA0">
        <CardTitle>{t('TOTAL NUMBER OF INDIVIDUALS REACHED')}</CardTitle>
        <Grid container justifyContent="space-between" alignItems="center">
          <Grid item data-cy="total-number-of-individuals-reached">
            <CardAmountLink onClick={() => setDialogOpen(true)}>
              {formatNumber(data?.total)}
            </CardAmountLink>
          </Grid>
          <Grid item>
            <IconContainer bg="#D9E2EF" color="#023F90">
              <PersonIcon fontSize="inherit" />
            </IconContainer>
          </Grid>
        </Grid>
      </DashboardCard>
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        scroll="paper"
        aria-labelledby="form-dialog-title"
        fullWidth
        maxWidth="md"
      >
        <DialogContent>
          <DialogContainer>
            <Box mb={6}>
              <Title mb={6}>
                {t('Individuals Reached by Age and Gender Groups')}
              </Title>
              <ChartWrapper>
                <IndividualsReachedByAgeAndGenderGroupsChart
                  data={chartDataIndividuals}
                />
              </ChartWrapper>
            </Box>
            <Box>
              <Title mb={6}>
                {t('Individuals with Disability Reached by Age Groups')}
              </Title>
              <IndividualsWithDisabilityReachedByAgeGroupsChart
                data={chartDataIndividualsDisability}
              />
            </Box>
          </DialogContainer>
        </DialogContent>
        <DialogFooter>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>CLOSE</Button>
          </DialogActions>
        </DialogFooter>
      </Dialog>
    </>
  );
}
