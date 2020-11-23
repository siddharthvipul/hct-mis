import React from 'react';
import { Button, Grid, IconButton, Typography } from '@material-ui/core';
import styled from 'styled-components';
import { Field, FieldArray } from 'formik';
import CalendarTodayRoundedIcon from '@material-ui/icons/CalendarTodayRounded';
import camelCase from 'lodash/camelCase';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import { FormikSelectField } from '../../shared/Formik/FormikSelectField';
import { FormikDateField } from '../../shared/Formik/FormikDateField';
import {
  AllAddIndividualFieldsQuery,
  useAllAddIndividualFieldsQuery,
} from '../../__generated__/graphql';
import { LoadingComponent } from '../LoadingComponent';
import { FormikCheckboxField } from '../../shared/Formik/FormikCheckboxField';
import { AddCircleOutline, Delete } from '@material-ui/icons';

const Title = styled.div`
  width: 100%;
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;
const AddIcon = styled(AddCircleOutline)`
  margin-right: 10px;
`;

export interface AddIndividualDataChangeFieldProps {
  field: AllAddIndividualFieldsQuery['allAddIndividualsFieldsAttributes'][number];
}
export const AddIndividualDataChangeField = ({
  field,
}: AddIndividualDataChangeFieldProps): React.ReactElement => {
  let fieldProps;
  switch (field.type) {
    case 'STRING':
      fieldProps = {
        component: FormikTextField,
      };
      break;
    case 'SELECT_ONE':
      fieldProps = {
        choices: field.choices,
        component: FormikSelectField,
      };
      break;
    case 'SELECT_MANY':
      fieldProps = {
        choices: field.choices,
        component: FormikSelectField,
        multiple: true,
      };
      break;
    case 'SELECT_MULTIPLE':
      fieldProps = {
        choices: field.choices,
        component: FormikSelectField,
      };
      break;
    case 'DATE':
      fieldProps = {
        component: FormikDateField,
        decoratorEnd: <CalendarTodayRoundedIcon color='disabled' />,
      };
      break;

    case 'BOOL':
      fieldProps = {
        component: FormikCheckboxField,
      };
      break;
    default:
      fieldProps = {};
  }
  return (
    <>
      <Grid item xs={6}>
        <Field
          name={`individualData.${camelCase(field.name)}`}
          fullWidth
          variant='outlined'
          label={field.labelEn}
          required={field.required}
          {...fieldProps}
        />
      </Grid>
      <Grid item xs={6} />
    </>
  );
};

export interface DocumentFieldProps {
  index: number;
  onDelete: () => {};
  countryChoices: AllAddIndividualFieldsQuery['countriesChoices'];
  documentTypeChoices: AllAddIndividualFieldsQuery['documentTypeChoices'];
}

export function DocumentField({
  index,
  onDelete,
  countryChoices,
  documentTypeChoices,
}: DocumentFieldProps): React.ReactElement {
  return (
    <>
      <Grid item xs={4}>
        <Field
          name={`individualData.documents[${index}].country`}
          fullWidth
          variant='outlined'
          label='Country'
          component={FormikSelectField}
          choices={countryChoices}
          required
        />
      </Grid>
      <Grid item xs={4}>
        <Field
          name={`individualData.documents[${index}].type`}
          fullWidth
          variant='outlined'
          label='Type'
          component={FormikSelectField}
          choices={documentTypeChoices}
          required
        />
      </Grid>
      <Grid item xs={3}>
        <Field
          name={`individualData.documents[${index}].number`}
          fullWidth
          variant='outlined'
          label='Document Number'
          component={FormikTextField}
          required
        />
      </Grid>
      <Grid item xs={1}>
        <IconButton onClick={onDelete}>
          <Delete />
        </IconButton>
      </Grid>
    </>
  );
}

export interface AddIndividualDataChangeProps {
  values;
}

export const AddIndividualDataChange = ({
  values,
}: AddIndividualDataChangeProps): React.ReactElement => {
  const { data, loading } = useAllAddIndividualFieldsQuery();
  if (loading) {
    return <LoadingComponent />;
  }
  return (
    <>
      <Title>
        <Typography variant='h6'>Individual Data</Typography>
      </Title>
      <Grid container spacing={3}>
        {data.allAddIndividualsFieldsAttributes.map((item) => (
          <AddIndividualDataChangeField field={item} />
        ))}
      </Grid>
      <Grid container spacing={3}>
        <FieldArray
          name='individualData.documents'
          render={(arrayHelpers) => {
            return (
              <>
                {values.individualData?.documents?.map((item, index) => (
                  <DocumentField
                    index={index}
                    onDelete={() => arrayHelpers.remove(index)}
                    countryChoices={data.countriesChoices}
                    documentTypeChoices={data.documentTypeChoices}
                  />
                ))}

                <Grid item xs={8} />
                <Grid item xs={4}>
                  <Button
                    color='primary'
                    onClick={() => {
                      arrayHelpers.push({
                        country: null,
                        type: null,
                        number: '',
                      });
                    }}
                  >
                    <AddIcon />
                    Add Document
                  </Button>
                </Grid>
              </>
            );
          }}
        />
      </Grid>
    </>
  );
};
