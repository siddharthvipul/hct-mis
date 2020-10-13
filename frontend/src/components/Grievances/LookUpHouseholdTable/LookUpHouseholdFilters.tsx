import React from 'react';
import styled from 'styled-components';
import { InputAdornment, MenuItem, TextField } from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import GroupIcon from '@material-ui/icons/Group';
import FlashOnIcon from '@material-ui/icons/FlashOn';
import FormControl from '@material-ui/core/FormControl';
import AssignmentIndRoundedIcon from '@material-ui/icons/AssignmentIndRounded';
import {
  HouseholdChoiceDataQuery,
  ProgramNode,
} from '../../../__generated__/graphql';
import { ContainerWithBorder } from '../../ContainerWithBorder';
import InputLabel from '../../../shared/InputLabel';
import Select from '../../../shared/Select';
import { AdminAreasAutocomplete } from '../../population/AdminAreaAutocomplete';

const TextContainer = styled(TextField)`
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
  input[type='number'] {
    -moz-appearance: textfield;
  }
`;
const StyledFormControl = styled(FormControl)`
  width: 232px;
  color: #5f6368;
  border-bottom: 0;
`;

const SearchTextField = styled(TextField)`
  flex: 1;
  && {
    min-width: 150px;
  }
`;

const StartInputAdornment = styled(InputAdornment)`
  margin-right: 0;
`;

interface LookUpHouseholdFiltersProps {
  onFilterChange;
  filter;
  programs: ProgramNode[];
  choicesData: HouseholdChoiceDataQuery;
}
export function LookUpHouseholdFilters({
  onFilterChange,
  filter,
  programs,
  choicesData,
}: LookUpHouseholdFiltersProps): React.ReactElement {
  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });
  return (
    <ContainerWithBorder>
      <SearchTextField
        label='Search'
        variant='outlined'
        margin='dense'
        onChange={(e) => handleFilterChange(e, 'text')}
        InputProps={{
          startAdornment: (
            <InputAdornment position='start'>
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        data-cy='filters-search'
      />
      <StyledFormControl variant='outlined' margin='dense'>
        <InputLabel>Programme</InputLabel>
        <Select
          /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
          // @ts-ignore
          onChange={(e) => handleFilterChange(e, 'program')}
          variant='outlined'
          label='Programme'
          value={filter.program || ''}
          InputProps={{
            startAdornment: (
              <StartInputAdornment position='start'>
                <FlashOnIcon />
              </StartInputAdornment>
            ),
          }}
        >
          <MenuItem value=''>
            <em>None</em>
          </MenuItem>
          {programs.map((program) => (
            <MenuItem key={program.id} value={program.id}>
              {program.name}
            </MenuItem>
          ))}
        </Select>
      </StyledFormControl>
      <StyledFormControl variant='outlined' margin='dense'>
        <InputLabel>Residence Status</InputLabel>
        <Select
          /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
          // @ts-ignore
          onChange={(e) => handleFilterChange(e, 'residenceStatus')}
          variant='outlined'
          label='Residence Status'
          value={filter.residenceStatus || ''}
          InputProps={{
            startAdornment: (
              <StartInputAdornment position='start'>
                <AssignmentIndRoundedIcon />
              </StartInputAdornment>
            ),
          }}
          SelectDisplayProps={{
            'data-cy': 'filters-residence-status',
          }}
          MenuProps={{
            'data-cy': 'filters-residence-status-options',
          }}
        >
          <MenuItem value=''>
            <em>None</em>
          </MenuItem>
          {choicesData.residenceStatusChoices.map((program) => (
            <MenuItem key={program.value} value={program.value}>
              {program.name}
            </MenuItem>
          ))}
        </Select>
      </StyledFormControl>
      <AdminAreasAutocomplete
        value={filter.adminArea}
        onChange={(e, option) => {
          if (!option) {
            onFilterChange({ ...filter, adminArea: undefined });
            return;
          }
          onFilterChange({ ...filter, adminArea: option.node.id });
        }}
      />
      <TextContainer
        id='minFilter'
        value={filter.householdSize.min}
        variant='outlined'
        margin='dense'
        label='Household size'
        onChange={(e) =>
          onFilterChange({
            ...filter,
            householdSize: {
              ...filter.householdSize,
              min: e.target.value || undefined,
            },
          })
        }
        type='number'
        InputProps={{
          startAdornment: (
            <InputAdornment position='start'>
              <GroupIcon />
            </InputAdornment>
          ),
        }}
      />
      to
      <TextContainer
        id='maxFilter'
        value={filter.householdSize.max}
        variant='outlined'
        margin='dense'
        label='Household size'
        onChange={(e) =>
          onFilterChange({
            ...filter,
            householdSize: {
              ...filter.householdSize,
              max: e.target.value || undefined,
            },
          })
        }
        type='number'
        InputProps={{
          startAdornment: (
            <InputAdornment position='start'>
              <GroupIcon />
            </InputAdornment>
          ),
        }}
      />
    </ContainerWithBorder>
  );
}
