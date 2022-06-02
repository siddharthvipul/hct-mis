import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  Grid,
  MenuItem,
} from '@material-ui/core';
import FlashOnIcon from '@material-ui/icons/FlashOn';
import WcIcon from '@material-ui/icons/Wc';
import { KeyboardDatePicker } from '@material-ui/pickers';
import moment from 'moment';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { ContainerWithBorder } from '../../../core/ContainerWithBorder';
import { FieldLabel } from '../../../core/FieldLabel';
import { SearchTextField } from '../../../core/SearchTextField';
import { SelectFilter } from '../../../core/SelectFilter';
import { AdminAreaAutocomplete } from '../../../population/AdminAreaAutocomplete';

interface LookUpIndividualFiltersProps {
  onFilterChange;
  filter;
  programs;
  setFilterIndividualApplied?;
  individualFilterInitial?;
  household?;
}
export function LookUpIndividualFilters({
  onFilterChange,
  filter,
  programs,
  setFilterIndividualApplied,
  individualFilterInitial,
  household,
}: LookUpIndividualFiltersProps): React.ReactElement {
  const { t } = useTranslation();
  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });
  return (
    <ContainerWithBorder>
      <Grid container alignItems='flex-end' spacing={3}>
        <Grid item>
          <SearchTextField
            label={t('Search')}
            value={filter.search}
            onChange={(e) => handleFilterChange(e, 'search')}
            data-cy='filters-search'
          />
        </Grid>
        <Grid item>
          <SelectFilter
            onChange={(e) => handleFilterChange(e, 'programs')}
            label={t('Programme')}
            value={filter.programs || []}
            icon={<FlashOnIcon />}
          >
            <MenuItem value=''>
              <em>{t('None')}</em>
            </MenuItem>
            {programs.map((program) => (
              <MenuItem key={program.id} value={program.id}>
                {program.name}
              </MenuItem>
            ))}
          </SelectFilter>
        </Grid>
        <Grid item>
          <Box display='flex' flexDirection='column'>
            <FieldLabel>{t('Registration Date')}</FieldLabel>
            <KeyboardDatePicker
              variant='inline'
              inputVariant='outlined'
              margin='dense'
              placeholder={t('From')}
              autoOk
              onChange={(date) =>
                onFilterChange({
                  ...filter,
                  lastRegistrationDate: {
                    ...filter.lastRegistrationDate,
                    min: date ? moment(date).format('YYYY-MM-DD') : null,
                  },
                })
              }
              value={filter.lastRegistrationDate.min || null}
              format='YYYY-MM-DD'
              InputAdornmentProps={{ position: 'end' }}
            />
          </Box>
        </Grid>
        <Grid item>
          <KeyboardDatePicker
            variant='inline'
            inputVariant='outlined'
            margin='dense'
            placeholder={t('To')}
            autoOk
            onChange={(date) =>
              onFilterChange({
                ...filter,
                lastRegistrationDate: {
                  ...filter.lastRegistrationDate,
                  max: date ? moment(date).format('YYYY-MM-DD') : null,
                },
              })
            }
            value={filter.lastRegistrationDate.max || null}
            format='YYYY-MM-DD'
            InputAdornmentProps={{ position: 'end' }}
          />
        </Grid>
        <Grid item>
          <SelectFilter
            onChange={(e) => handleFilterChange(e, 'status')}
            multiple
            label={t('Status')}
            value={filter.status || []}
          >
            {[
              { value: 'ACTIVE', name: 'Active' },
              { value: 'WITHDRAWN', name: 'Withdrawn' },
              { value: 'DUPLICATE', name: 'Duplicate' },
            ].map((item) => {
              return (
                <MenuItem key={item.value} value={item.value}>
                  {item.name}
                </MenuItem>
              );
            })}
          </SelectFilter>
        </Grid>
        <Grid item>
          <AdminAreaAutocomplete
            onFilterChange={onFilterChange}
            name='admin2'
            value={filter.admin2}
          />
        </Grid>
        <Grid item>
          <SelectFilter
            onChange={(e) => handleFilterChange(e, 'sex')}
            value={filter.sex || ''}
            label={t('Gender')}
            icon={<WcIcon />}
            SelectDisplayProps={{
              'data-cy': 'filters-sex',
            }}
            MenuProps={{
              'data-cy': 'filters-sex-options',
            }}
          >
            <MenuItem value=''>
              <em>{t('None')}</em>
            </MenuItem>
            <MenuItem value='MALE'>{t('Male')}</MenuItem>
            <MenuItem value='FEMALE'>{t('Female')}</MenuItem>
          </SelectFilter>
        </Grid>
        {household && (
          <Grid item>
            <FormControlLabel
              control={
                <Checkbox
                  checked={filter.household}
                  color='primary'
                  onChange={(e) => {
                    if (e.target.checked) {
                      onFilterChange({ ...filter, household: household.id });
                    } else {
                      onFilterChange({ ...filter, household: null });
                    }
                  }}
                />
              }
              label={t('Show only Individuals from this household')}
            />
          </Grid>
        )}

        <Grid container justify='flex-end'>
          <Button
            color='primary'
            onClick={() => {
              setFilterIndividualApplied(individualFilterInitial);
              onFilterChange(individualFilterInitial);
            }}
          >
            {t('Clear')}
          </Button>
          <Button
            color='primary'
            variant='outlined'
            onClick={() => setFilterIndividualApplied(filter)}
          >
            {t('Apply')}
          </Button>
        </Grid>
      </Grid>
    </ContainerWithBorder>
  );
}
