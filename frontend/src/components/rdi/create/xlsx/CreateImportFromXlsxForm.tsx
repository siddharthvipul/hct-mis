/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import * as Yup from 'yup';
import { Field, FormikProvider, useFormik } from 'formik';
import { CircularProgress } from '@material-ui/core';
import styled from 'styled-components';
import { useHistory } from 'react-router-dom';
import { useBusinessArea } from '../../../../hooks/useBusinessArea';
import { FormikTextField } from '../../../../shared/Formik/FormikTextField';
import { ScreenBeneficiaryField } from '../ScreenBeneficiaryField';
import {
  ImportDataStatus,
  useCreateRegistrationXlsxImportMutation,
} from '../../../../__generated__/graphql';
import { useSnackbar } from '../../../../hooks/useSnackBar';
import { handleValidationErrors } from '../../../../utils/utils';
import { useSaveXlsxImportDataAndCheckStatus } from './useSaveXlsxImportDataAndCheckStatus';
import { XlsxImportDataRepresentation } from './XlsxImportDataRepresentation';
import { DropzoneField } from './DropzoneField';

const CircularProgressContainer = styled.div`
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
`;

const validationSchema = Yup.object().shape({
  name: Yup.string()
    .required('Title is required')
    .min(2, 'Too short')
    .max(255, 'Too long'),
});
export function CreateImportFromXlsxForm({
  setSubmitForm,
  setSubmitDisabled,
}): React.ReactElement {
  const {
    saveAndStartPolling,
    stopPollingImportData,
    loading: saveXlsxLoading,
    xlsxImportData,
  } = useSaveXlsxImportDataAndCheckStatus();
  const businessAreaSlug = useBusinessArea();
  const { showMessage } = useSnackbar();
  const { t } = useTranslation();
  const history = useHistory();
  const [createImport] = useCreateRegistrationXlsxImportMutation();
  const onSubmit = async (values, { setFieldError }): Promise<void> => {
    try {
      const data = await createImport({
        variables: {
          registrationDataImportData: {
            importDataId: xlsxImportData.id,
            name: values.name,
            screenBeneficiary: values.screenBeneficiary,
            businessAreaSlug,
          },
        },
      });
      history.push(
        `/${businessAreaSlug}/registration-data-import/${data.data.registrationXlsxImport.registrationDataImport.id}`,
      );
    } catch (error) {
      const { nonValidationErrors } = handleValidationErrors(
        'registrationXlsxImport',
        error,
        setFieldError,
        showMessage,
      );
      if (nonValidationErrors.length > 0) {
        showMessage(
          t('Unexpected problem while creating Registration Data Import'),
        );
      }
    }
  };
  const formik = useFormik({
    initialValues: {
      name: '',
      screenBeneficiary: false,
      file: null,
    },
    validationSchema,
    onSubmit,
  });
  // eslint-disable-next-line @typescript-eslint/require-await
  const saveXlsxInputData = async (): Promise<void> => {
    if (!formik.values.file) {
      return;
    }
    setSubmitDisabled(true);
    stopPollingImportData();
    await saveAndStartPolling({
      businessAreaSlug,
      file: formik.values.file,
    });
  };
  useEffect(() => stopPollingImportData, []);
  useEffect(() => {
    saveXlsxInputData();
  }, [formik.values.file]);
  useEffect(() => {
    setSubmitForm(formik.submitForm);
  }, [formik.submitForm]);
  useEffect(() => {
    if (xlsxImportData?.status === ImportDataStatus.Finished) {
      setSubmitDisabled(false);
    }
  }, [xlsxImportData]);
  return (
    <div>
      <FormikProvider value={formik}>
        <DropzoneField loading={saveXlsxLoading} />
        <Field
          name='name'
          fullWidth
          label={t('Title')}
          required
          variant='outlined'
          component={FormikTextField}
        />
        <ScreenBeneficiaryField />
        <CircularProgressContainer>
          {saveXlsxLoading && <CircularProgress />}
        </CircularProgressContainer>
        <XlsxImportDataRepresentation
          xlsxImportData={xlsxImportData}
          loading={saveXlsxLoading}
        />
      </FormikProvider>
    </div>
  );
}