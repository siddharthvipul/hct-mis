import { Grid, IconButton } from '@material-ui/core';
import { Delete } from '@material-ui/icons';
import { useLocation } from 'react-router-dom';
import { Field } from 'formik';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { FormikSelectField } from '../../shared/Formik/FormikSelectField';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import { AllAddIndividualFieldsQuery } from '../../__generated__/graphql';
import { GrievanceDocumentPhotoModalEditable } from './GrievancesPhotoModals/GrievanceDocumentPhotoModalEditable';

export interface DocumentFieldProps {
  index: number;
  baseName: string;
  onDelete: () => {};
  countryChoices: AllAddIndividualFieldsQuery['countriesChoices'];
  documentTypeChoices: AllAddIndividualFieldsQuery['documentTypeChoices'];
  isEdited?: boolean;
  setFieldValue?;
  photoSrc?: string;
}

export function DocumentField({
  index,
  baseName,
  onDelete,
  countryChoices,
  documentTypeChoices,
  isEdited,
  setFieldValue,
  photoSrc,
}: DocumentFieldProps): React.ReactElement {
  const { t } = useTranslation();
  const location = useLocation();
  const isEditTicket = location.pathname.indexOf('edit-ticket') !== -1;

  return (
    <>
      <Grid item xs={3}>
        <Field
          name={`${baseName}[${index}].type`}
          fullWidth
          variant='outlined'
          label={t('Type')}
          component={FormikSelectField}
          choices={documentTypeChoices}
          required
          disabled={isEditTicket}
        />
      </Grid>
      <Grid item xs={2}>
        <Field
          name={`${baseName}[${index}].country`}
          fullWidth
          variant='outlined'
          label={t('Country')}
          component={FormikSelectField}
          choices={countryChoices}
          required
          disabled={isEditTicket}
        />
      </Grid>
      <Grid item xs={3}>
        <Field
          name={`${baseName}[${index}].number`}
          fullWidth
          variant='outlined'
          label={t('Document Number')}
          component={FormikTextField}
          required
          disabled={isEditTicket}
        />
      </Grid>
      <Grid item xs={3}>
        <GrievanceDocumentPhotoModalEditable
          photoSrc={photoSrc}
          setFieldValue={setFieldValue}
          fieldName={`${baseName}[${index}].photo`}
        />
      </Grid>
      {!isEdited ? (
        <Grid item xs={1}>
          <IconButton disabled={isEditTicket} onClick={onDelete}>
            <Delete />
          </IconButton>
        </Grid>
      ) : null}
    </>
  );
}
