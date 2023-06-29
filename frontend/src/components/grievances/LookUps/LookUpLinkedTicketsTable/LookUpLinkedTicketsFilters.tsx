import { Button, Grid, MenuItem } from '@material-ui/core';
import moment from 'moment';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { LookUpAdminAreaAutocomplete } from '../../../../shared/autocompletes/LookUpAdminAreaAutocomplete';
import { GrievancesChoiceDataQuery } from '../../../../__generated__/graphql';
import { ContainerWithBorder } from '../../../core/ContainerWithBorder';
import { DatePickerFilter } from '../../../core/DatePickerFilter';
import { SearchTextField } from '../../../core/SearchTextField';
import { SelectFilter } from '../../../core/SelectFilter';

interface LookUpLinkedTicketsFiltersProps {
  onFilterChange;
  filter;
  choicesData: GrievancesChoiceDataQuery;
  setFilterApplied?;
  filterInitial?;
}
export function LookUpLinkedTicketsFilters({
  onFilterChange,
  filter,
  choicesData,
  setFilterApplied,
  filterInitial,
}: LookUpLinkedTicketsFiltersProps): React.ReactElement {
  const { t } = useTranslation();
  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });
  return (
    <ContainerWithBorder>
      <Grid container alignItems='flex-end' spacing={3}>
        <Grid item xs={3}>
          <SearchTextField
            label={t('Search')}
            value={filter.search}
            onChange={(e) => handleFilterChange(e, 'search')}
            data-cy='filters-search'
          />
        </Grid>
        <Grid item xs={3}>
          <SelectFilter
            onChange={(e) => handleFilterChange(e, 'status')}
            label={t('Status')}
            value={filter.status || null}
            data-cy='filters-status'
          >
            <MenuItem value=''>
              <em>None</em>
            </MenuItem>
            {choicesData.grievanceTicketStatusChoices.map((item) => {
              return (
                <MenuItem key={item.value} value={item.value}>
                  {item.name}
                </MenuItem>
              );
            })}
          </SelectFilter>
        </Grid>
        <Grid item xs={3}>
          <SearchTextField
            label={t('FSP')}
            value={filter.fsp}
            onChange={(e) => handleFilterChange(e, 'fsp')}
            data-cy='filters-fsp'
          />
        </Grid>
        <Grid item xs={3}>
          <DatePickerFilter
            topLabel={t('Creation Date')}
            label='From'
            onChange={(date) =>
              onFilterChange({
                ...filter,
                createdAtRange: {
                  ...filter.createdAtRange,
                  min: moment(date)
                    .startOf('day')
                    .toISOString(),
                },
              })
            }
            value={filter.createdAtRange.min}
            data-cy='filters-creation-date-from'
          />
        </Grid>
        <Grid item xs={3}>
          <DatePickerFilter
            label={t('To')}
            onChange={(date) =>
              onFilterChange({
                ...filter,
                createdAtRange: {
                  ...filter.createdAtRange,
                  max: moment(date)
                    .endOf('day')
                    .toISOString(),
                },
              })
            }
            value={filter.createdAtRange.max}
            data-cy='filters-creation-date-to'
          />
        </Grid>
        <Grid item xs={3}>
          <LookUpAdminAreaAutocomplete
            onFilterChange={onFilterChange}
            name='admin'
            dataCy='filters-admin'
          />
        </Grid>
        <Grid container justifyContent='flex-end'>
          <Button
            color='primary'
            onClick={() => {
              setFilterApplied(filterInitial);
              onFilterChange(filterInitial);
            }}
          >
            {t('Clear')}
          </Button>
          <Button
            color='primary'
            variant='outlined'
            onClick={() => setFilterApplied(filter)}
          >
            {t('Apply')}
          </Button>
        </Grid>
      </Grid>
    </ContainerWithBorder>
  );
}
