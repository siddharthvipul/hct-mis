/* eslint-disable react-hooks/exhaustive-deps */
import React, { useCallback, useState } from 'react';
import styled from 'styled-components';
import * as Yup from 'yup';
import { useTranslation } from 'react-i18next';
import {
  Button,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from '@material-ui/core';
import ExitToAppRoundedIcon from '@material-ui/icons/ExitToAppRounded';
import { useDropzone } from 'react-dropzone';
import { Field, Form, Formik } from 'formik';
import get from 'lodash/get';
import {
  KoboErrorNode,
  SaveKoboImportDataMutation,
  UploadImportDataXlsxFileMutation,
  useAllKoboProjectsQuery,
  useCreateRegistrationKoboImportMutation,
  useCreateRegistrationXlsxImportMutation,
  useSaveKoboImportDataMutation,
  useUploadImportDataXlsxFileMutation,
  XlsxRowErrorNode,
} from '../../../__generated__/graphql';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { FormikTextField } from '../../../shared/Formik/FormikTextField';
import { LoadingComponent } from '../../../components/LoadingComponent';
import { Dialog } from '../../dialogs/Dialog';
import { DialogActions } from '../../dialogs/DialogActions';
import { ErrorsKobo } from './errors/KoboErrors';
import { Errors } from './errors/PlainErrors';
import { handleValidationErrors } from '../../../utils/utils';

const DialogTitleWrapper = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
`;

const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;

const ComboBox = styled(Select)`
  & {
    min-width: 200px;
  }
`;

const StyledInputLabel = styled(InputLabel)`
  background-color: #fff;
`;
const DropzoneContainer = styled.div`
  width: 100%;
  height: 100px;
  background-color: rgba(2, 62, 144, 0.1);
  color: #023e90;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.5px;
  line-height: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: ${({ theme }) => theme.spacing(5)}px;
  cursor: pointer;

  ${({ disabled }) => (disabled ? 'filter: grayscale(100%);' : '')}
`;

const StyledDialogFooter = styled(DialogFooter)`
  && {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
`;

function DropzoneField({ onChange, loading }): React.ReactElement {
  const onDrop = useCallback((acceptedFiles) => {
    onChange(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    disabled: loading,
    accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    onDrop,
  });
  const acceptedFilename =
    acceptedFiles.length > 0 ? acceptedFiles[0].name : null;
  return (
    <div>
      <DropzoneContainer {...getRootProps()} disabled={loading}>
        <LoadingComponent isLoading={loading} absolute />
        <input {...getInputProps()} data-cy='rdi-file-input' />
        {acceptedFilename || 'UPLOAD FILE'}
      </DropzoneContainer>
    </div>
  );
}

const validationSchema = Yup.object().shape({
  name: Yup.string()
    .required('Title is required')
    .min(2, 'Too short')
    .max(255, 'Too long'),
});

export function RegistrationDataImport(): React.ReactElement {
  const [open, setOpen] = useState(false);
  const [importType, setImportType] = useState();
  const [koboProject, setKoboProject] = useState();
  const { showMessage } = useSnackbar();
  const businessArea = useBusinessArea();
  const [
    uploadMutate,
    { data: uploadData, loading: fileLoading },
  ] = useUploadImportDataXlsxFileMutation();
  const [
    createRegistrationXlsxMutate,
    { loading: createLoading },
  ] = useCreateRegistrationXlsxImportMutation();
  const [
    saveKoboImportDataMutate,
    { loading: saveKoboLoading, data: koboImportData },
  ] = useSaveKoboImportDataMutation();
  const [
    createRegistrationKoboMutate,
  ] = useCreateRegistrationKoboImportMutation();
  const { data: koboProjectsData } = useAllKoboProjectsQuery({
    variables: { businessAreaSlug: businessArea },
  });
  const { t } = useTranslation();
  const xlsxErrors: UploadImportDataXlsxFileMutation['uploadImportDataXlsxFile']['errors'] = get(
    uploadData,
    'uploadImportDataXlsxFile.errors',
  );
  const koboErrors: SaveKoboImportDataMutation['saveKoboImportData']['errors'] =
    koboImportData?.saveKoboImportData?.errors;
  let counters = null;
  let disabled = true;
  if (uploadData?.uploadImportDataXlsxFile?.importData) {
    counters = (
      <>
        <div data-cy='import-available-households-counter'>
          {uploadData.uploadImportDataXlsxFile.importData.numberOfHouseholds}{' '}
          Households available to Import
        </div>
        <div data-cy='import-available-individuals-counter'>
          {uploadData.uploadImportDataXlsxFile.importData.numberOfIndividuals}{' '}
          Individuals available to Import
        </div>
      </>
    );
  }
  if (koboImportData?.saveKoboImportData?.importData) {
    counters = (
      <>
        <div>
          {koboImportData?.saveKoboImportData?.importData.numberOfHouseholds}{' '}
          Households available to Import
        </div>
        <div>
          {koboImportData?.saveKoboImportData?.importData.numberOfIndividuals}{' '}
          Individuals available to Import
        </div>
      </>
    );
  }
  let importTypeSpecificContent = null;
  if (importType === 'excel') {
    disabled = !uploadData || createLoading;
    importTypeSpecificContent = (
      <>
        <DropzoneField
          loading={fileLoading}
          onChange={(files) => {
            if (files.length === 0) {
              return;
            }
            const file = files[0];
            const fileSizeMB = file.size / (1024 * 1024);
            if (fileSizeMB > 200) {
              showMessage(
                `File size is to big. It should be under 200MB, File size is ${fileSizeMB}MB`,
              );
              return;
            }
            uploadMutate({
              variables: {
                file,
                businessAreaSlug: businessArea,
              },
            });
          }}
        />
        <Errors errors={xlsxErrors as XlsxRowErrorNode[]} />
      </>
    );
  } else if (importType === 'kobo') {
    disabled = saveKoboLoading || !koboImportData;
    const koboProjects = koboProjectsData?.allKoboProjects?.edges || [];
    importTypeSpecificContent = (
      <div>
        <FormControl variant='outlined' margin='dense'>
          <StyledInputLabel>Import from</StyledInputLabel>
          <ComboBox
            value={koboProject}
            variant='outlined'
            label='Kobo Project'
            onChange={(e) => {
              setKoboProject(e.target.value);
              saveKoboImportDataMutate({
                variables: {
                  projectId: e.target.value,
                  businessAreaSlug: businessArea,
                },
              });
            }}
            fullWidth
          >
            {koboProjects.map((item) => (
              <MenuItem key={item.node.id} value={item.node.id}>
                {item.node.name}
              </MenuItem>
            ))}
          </ComboBox>
        </FormControl>
        <ErrorsKobo errors={koboErrors as KoboErrorNode[]} />
      </div>
    );
  }
  if (importType === 'kobo') {
    disabled =
      !koboImportData ||
      (koboImportData?.saveKoboImportData?.importData?.numberOfHouseholds ===
        0 &&
        koboImportData?.saveKoboImportData?.importData?.numberOfIndividuals ===
          0);
  }
  return (
    <span>
      <Button
        variant='contained'
        color='primary'
        startIcon={<ExitToAppRoundedIcon />}
        onClick={() => setOpen(true)}
        data-cy='button-import'
      >
        IMPORT
      </Button>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        scroll='paper'
        aria-labelledby='form-dialog-title'
      >
        <Formik
          validationSchema={validationSchema}
          onSubmit={async (values, { setFieldError }) => {
            try {
              let rdiId = null;
              if (importType === 'kobo') {
                const { data } = await createRegistrationKoboMutate({
                  variables: {
                    registrationDataImportData: {
                      importDataId:
                        koboImportData.saveKoboImportData.importData.id,
                      name: values.name,
                      businessAreaSlug: businessArea,
                    },
                  },
                });
                rdiId =
                  data?.registrationKoboImport?.registrationDataImport?.id;
              } else if (importType === 'excel') {
                const { data } = await createRegistrationXlsxMutate({
                  variables: {
                    registrationDataImportData: {
                      importDataId:
                        uploadData.uploadImportDataXlsxFile.importData.id,
                      name: values.name,
                      businessAreaSlug: businessArea,
                    },
                  },
                });
                rdiId =
                  data?.registrationXlsxImport?.registrationDataImport?.id;
              }

              showMessage('Registration', {
                pathname: `/${businessArea}/registration-data-import/${rdiId}`,
                historyMethod: 'push',
              });
            } catch (e) {
              let nonValidationErrors;
              if (importType === 'kobo') {
                  nonValidationErrors  = handleValidationErrors(
                  'registrationKoboImport',
                  e,
                  setFieldError,
                  showMessage,
                ).nonValidationErrors;
              }else if (importType === 'excel'){
                  nonValidationErrors  = handleValidationErrors(
                  'registrationXlsxImport',
                  e,
                  setFieldError,
                  showMessage,
                ).nonValidationErrors;
              }

              if (nonValidationErrors.length > 0) {
                showMessage(
                  'Unexpected problem while creating Target Population',
                );
              }
            }
          }}
          initialValues={{ name: '' }}
        >
          {({ submitForm }) => (
            <Form>
              <DialogTitleWrapper>
                <DialogTitle id='scroll-dialog-title'>
                  {t('Select File to Import')}
                </DialogTitle>
              </DialogTitleWrapper>
              <DialogContent>
                <FormControl variant='outlined' margin='dense'>
                  <StyledInputLabel>Import from</StyledInputLabel>
                  <ComboBox
                    value={importType}
                    variant='outlined'
                    label=''
                    onChange={(e) => setImportType(e.target.value)}
                    fullWidth
                    SelectDisplayProps={{
                      'data-cy': 'select-import-from',
                    }}
                    MenuProps={{
                      'data-cy': 'select-import-from-options',
                    }}
                  >
                    <MenuItem key='excel' value='excel'>
                      Excel
                    </MenuItem>
                    <MenuItem key='kobo' value='kobo'>
                      Kobo
                    </MenuItem>
                  </ComboBox>
                </FormControl>
                {importTypeSpecificContent}
                {counters}
                <Field
                  name='name'
                  fullWidth
                  label='Title'
                  required
                  variant='outlined'
                  component={FormikTextField}
                />
              </DialogContent>
              <StyledDialogFooter data-cy='dialog-actions-container'>
                <Button
                  variant='text'
                  color='primary'
                  component='a'
                  href='/api/download-template'
                  onClick={(event) => {
                    /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
                    // @ts-ignore
                    if (window.Cypress) {
                      event.preventDefault();
                    }
                  }}
                  data-cy='a-download-template'
                >
                  DOWNLOAD TEMPLATE
                </Button>
                <DialogActions>
                  <Button onClick={() => setOpen(false)}>CANCEL</Button>
                  <Button
                    type='submit'
                    color='primary'
                    variant='contained'
                    disabled={disabled}
                    onClick={() => {
                      submitForm();
                    }}
                    data-cy='button-import'
                  >
                    {t('IMPORT')}
                  </Button>
                </DialogActions>
              </StyledDialogFooter>
            </Form>
          )}
        </Formik>
      </Dialog>
    </span>
  );
}
