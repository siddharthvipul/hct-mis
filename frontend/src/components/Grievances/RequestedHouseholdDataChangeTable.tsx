import React, { ReactElement, useEffect, useState } from 'react';
import styled from 'styled-components';
import Table from '@material-ui/core/Table';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import camelCase from 'lodash/camelCase';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import mapKeys from 'lodash/mapKeys';
import { Checkbox, makeStyles } from '@material-ui/core';
import {
  AllEditHouseholdFieldsQuery,
  GrievanceTicketQuery,
  useAllEditHouseholdFieldsQuery,
} from '../../__generated__/graphql';
import { LoadingComponent } from '../LoadingComponent';
import { GRIEVANCE_TICKET_STATES } from '../../utils/constants';
import { useArrayToDict } from '../../hooks/useArrayToDict';

const Capitalize = styled.span`
  text-transform: capitalize;
`;
const GreenIcon = styled.div`
  color: #28cb15;
`;

export interface CurrentValueProps {
  field: AllEditHouseholdFieldsQuery['allEditHouseholdFieldsAttributes'][number];
  value;
}

export function CurrentValue({
  field,
  value,
}: CurrentValueProps): React.ReactElement {
  let displayValue = value;
  if (field?.name === 'country' || field?.name === 'country_origin') {
    displayValue = value || '-';
  } else {
    switch (field?.type) {
      case 'SELECT_ONE':
        displayValue =
          field.choices.find((item) => item.value === value)?.labelEn || '-';
        break;
      case 'BOOL':
        /* eslint-disable-next-line no-nested-ternary */
        displayValue = value === null ? '-' : value ? 'Yes' : 'No';
        break;
      default:
        displayValue = value;
    }
  }
  return <>{displayValue || '-'}</>;
}
export function NewValue({
  field,
  value,
}: CurrentValueProps): React.ReactElement {
  let displayValue = value;
  switch (field?.type) {
    case 'SELECT_ONE':
      displayValue =
        field.choices.find((item) => item.value === value)?.labelEn || '-';
      break;
    case 'BOOL':
      /* eslint-disable-next-line no-nested-ternary */
      displayValue = value === null ? '-' : value ? 'Yes' : 'No';
      break;
    default:
      displayValue = value;
  }
  return <>{displayValue || '-'}</>;
}
interface RequestedHouseholdDataChangeTableProps {
  ticket: GrievanceTicketQuery['grievanceTicket'];
  setFieldValue;
  isEdit;
  values;
}
export function RequestedHouseholdDataChangeTable({
  setFieldValue,
  ticket,
  isEdit,
  values,
}: RequestedHouseholdDataChangeTableProps): ReactElement {
  const useStyles = makeStyles(() => ({
    table: {
      minWidth: 100,
    },
  }));
  const classes = useStyles();
  const { data, loading } = useAllEditHouseholdFieldsQuery();
  const selectedBioData = values.selected;
  const { selectedFlexFields } = values;

  const entries = Object.entries(
    ticket.householdDataUpdateTicketDetails.householdData,
  );
  const fieldsDict = useArrayToDict(
    data?.allEditHouseholdFieldsAttributes,
    'name',
    '*',
  );
  const countriesDict = useArrayToDict(data?.countriesChoices, 'value', 'name');
  if (loading || !fieldsDict || !countriesDict) {
    return <LoadingComponent />;
  }

  const handleFlexFields = (name, selected) => {
    const newSelected = [...selectedFlexFields];
    const selectedIndex = newSelected.indexOf(name);
    if (selectedIndex !== -1) {
      newSelected.splice(selectedIndex, 1);
    } else {
      newSelected.push(name);
    }
    setFieldValue('selectedFlexFields', newSelected);
  };
  const handleSelectBioData = (name, selected) => {
    const newSelected = [...selectedBioData];
    const selectedIndex = newSelected.indexOf(name);
    if (selectedIndex !== -1) {
      newSelected.splice(selectedIndex, 1);
    } else {
      newSelected.push(name);
    }
    setFieldValue('selected', newSelected);
  };


  const isSelected = (name: string): boolean => selectedBioData.includes(name);
  const isSelectedFlexfields = (name: string): boolean =>
    selectedFlexFields.includes(name);
  return (
    <div>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell align='left' />
            <TableCell align='left'>Type of Data</TableCell>
            <TableCell align='left'>
              {ticket.status === GRIEVANCE_TICKET_STATES.CLOSED
                ? 'Previous'
                : 'Current'}{' '}
              Value
            </TableCell>
            <TableCell align='left'>New Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {entries.map((row, index) => {
            const fieldName = camelCase(row[0]);
            const field = fieldsDict[row[0]];
            const isItemSelected = isSelected(fieldName);
            const labelId = `enhanced-table-checkbox-${index}`;
            const valueDetails = mapKeys(row[1], (v, k) => camelCase(k)) as {
              value: string;
              previousValue: string;
              approveStatus: boolean;
            };
            const previousValue =
              fieldName === 'country' || fieldName === 'countryOrigin'
                ? countriesDict[valueDetails.previousValue]
                : valueDetails.previousValue;
            const currentValue =
              ticket.status === GRIEVANCE_TICKET_STATES.CLOSED
                ? previousValue
                : ticket.householdDataUpdateTicketDetails.household[fieldName];
            return (
              <TableRow
                role='checkbox'
                aria-checked={isItemSelected}
                key={fieldName}
              >
                <TableCell>
                  {isEdit ? (
                    <Checkbox
                      onChange={(event) =>
                        handleSelectBioData(fieldName, event.target.checked)
                      }
                      color='primary'
                      disabled={
                        ticket.status !== GRIEVANCE_TICKET_STATES.FOR_APPROVAL
                      }
                      checked={isItemSelected}
                      inputProps={{ 'aria-labelledby': labelId }}
                    />
                  ) : (
                    isItemSelected && (
                      <GreenIcon>
                        <CheckCircleIcon />
                      </GreenIcon>
                    )
                  )}
                </TableCell>
                <TableCell id={labelId} scope='row' align='left'>
                  <Capitalize>{row[0].replaceAll('_', ' ')}</Capitalize>
                </TableCell>
                <TableCell align='left'>
                  <CurrentValue field={field} value={currentValue} />
                </TableCell>
                <TableCell align='left'>
                  <NewValue field={field} value={valueDetails.value} />
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
