import { Grid, MenuItem } from '@material-ui/core';
import moment from 'moment';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useFeedbackIssueTypeChoicesQuery } from '../../../../__generated__/graphql';
import { ContainerWithBorder } from '../../../core/ContainerWithBorder';
import { DatePickerFilter } from '../../../core/DatePickerFilter';
import { LoadingComponent } from '../../../core/LoadingComponent';
import { SearchTextField } from '../../../core/SearchTextField';
import { SelectFilter } from '../../../core/SelectFilter';
import { AssigneeAutocomplete } from '../../../grievances/GrievancesTable/AssigneeAutocomplete';

interface FeedbackFiltersProps {
  onFilterChange;
  filter;
}
export const FeedbackFilters = ({
  onFilterChange,
  filter,
}: FeedbackFiltersProps): React.ReactElement => {
  const { t } = useTranslation();
  const {
    data: choicesData,
    loading: choicesLoading,
  } = useFeedbackIssueTypeChoicesQuery();

  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });

  if (choicesLoading) return <LoadingComponent />;

  return (
    <ContainerWithBorder>
      <Grid container alignItems='center' spacing={3}>
        <Grid xs={4}>
          <SearchTextField
            value={filter.feedbackId || ''}
            label='Search'
            onChange={(e) => handleFilterChange(e, 'feedbackId')}
            data-cy='filters-search'
            fullWidth
          />
        </Grid>
        <Grid item xs={3}>
          <SelectFilter
            onChange={(e) => handleFilterChange(e, 'issueType')}
            label={t('Issue Type')}
            value={filter.issueType || ''}
            fullWidth
          >
            <MenuItem value=''>
              <em>{t('None')}</em>
            </MenuItem>
            {choicesData.feedbackIssueTypeChoices.map((issueType) => (
              <MenuItem key={issueType.name} value={issueType.value}>
                {issueType.name}
              </MenuItem>
            ))}
          </SelectFilter>
        </Grid>
        <Grid item xs={3}>
          <AssigneeAutocomplete
            onFilterChange={onFilterChange}
            name='createdBy'
            label={t('Created by')}
            fullWidth
          />
        </Grid>
        <Grid container item xs={3} spacing={3} alignItems='flex-end'>
          <Grid item xs={6}>
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
            />
          </Grid>
          <Grid item xs={6}>
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
            />
          </Grid>
        </Grid>
      </Grid>
    </ContainerWithBorder>
  );
};
