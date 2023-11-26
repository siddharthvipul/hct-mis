import { Box, Button, Step, StepButton, Stepper } from '@material-ui/core';
import { Formik } from 'formik';
import React, { ReactElement, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useParams } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import {
  useAllAreasTreeQuery,
  useProgramQuery,
  useUpdateProgramMutation,
} from '../../../__generated__/graphql';
import { ALL_LOG_ENTRIES_QUERY } from '../../../apollo/queries/core/AllLogEntries';
import { PROGRAM_QUERY } from '../../../apollo/queries/program/Program';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { PageHeader } from '../../../components/core/PageHeader';
import { DetailsStep } from '../../../components/programs/CreateProgram/DetailsStep';
import { PartnersStep } from '../../../components/programs/CreateProgram/PartnersStep';
import { useBaseUrl } from '../../../hooks/useBaseUrl';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { decodeIdString } from '../../../utils/utils';
import { programValidationSchema } from '../../../components/programs/CreateProgram/programValidationSchema';

export const EditProgramPage = (): ReactElement => {
  const { t } = useTranslation();
  const { id } = useParams();

  const [step, setStep] = useState(0);
  const { showMessage } = useSnackbar();
  const { baseUrl, businessArea } = useBaseUrl();
  const { data: treeData, loading: treeLoading } = useAllAreasTreeQuery({
    variables: { businessArea },
  });
  const { data, loading: loadingProgram } = useProgramQuery({
    variables: { id },
    fetchPolicy: 'cache-and-network',
  });
  const [mutate] = useUpdateProgramMutation({
    refetchQueries: [
      {
        query: ALL_LOG_ENTRIES_QUERY,
        variables: {
          objectId: decodeIdString(id),
          count: 5,
          businessArea,
        },
      },
    ],
    update(cache, { data: { updateProgram } }) {
      cache.writeQuery({
        query: PROGRAM_QUERY,
        variables: { id },
        data: { program: updateProgram.program },
      });
    },
  });

  if (!data) return null;
  if (loadingProgram) return <LoadingComponent />;
  const {
    name,
    startDate,
    endDate,
    sector,
    dataCollectingType,
    description,
    budget = '0.00',
    administrativeAreasOfImplementation,
    populationGoal = 0,
    cashPlus = false,
    frequencyOfPayments = 'REGULAR',
    version,
  } = data.program;

  const handleSubmit = async (values): Promise<void> => {
    try {
      const response = await mutate({
        variables: {
          programData: {
            id,
            ...values,
            budget: parseFloat(values.budget).toFixed(2),
          },
          version,
        },
      });
      showMessage(t('Programme edited.'), {
        pathname: `/${baseUrl}/details/${response.data.updateProgram.program.id}`,
      });
    } catch (e) {
      e.graphQLErrors.map((x) => showMessage(x.message));
    }
  };

  //TODO: remove this
  const partners = [
    {
      id: '9bef9d07-d45b-4291-ade6-3227311f3cea',
      partner: 'examplePartner1',
      areaAccess: 'ADMIN_AREA',
      adminAreas: [
        '6d49768f-e5fc-4f33-92f0-5004c31dcaf5',
        '705f5c09-484a-41d7-9aa4-6c7418d4ec80',
        '1841435e-d530-4f87-8aa6-7b1828f4c4a3',
        'e3c08a14-c47d-4b7a-b9e4-893dccac9622',
      ],
    },
    {
      id: '423a9e1c-4e21-485e-801d-808091e9808f',
      areaAccess: 'BUSINESS_AREA',
    },
    {
      id: 'ef356928-fbdf-442d-90e9-d444a2488e77',
    },
  ];

  const initialValues = {
    name,
    startDate,
    endDate,
    sector,
    dataCollectingTypeCode: dataCollectingType?.code,
    description,
    budget,
    administrativeAreasOfImplementation,
    populationGoal,
    cashPlus,
    frequencyOfPayments,
    partners,
  };

  if (treeLoading) return <LoadingComponent />;
  if (!treeData) return null;

  const { allAreasTree } = treeData;

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={(values) => {
        handleSubmit(values);
      }}
      validationSchema={programValidationSchema(t)}
    >
      {({ submitForm, values }) => {
        return (
          <>
            <PageHeader title={`${t('Edit Programme')}: (${name})`}>
              <Box display='flex' alignItems='center'>
                <Button component={Link} to={`/${baseUrl}/details/${id}`}>
                  {t('Cancel')}
                </Button>
                <Button
                  variant='contained'
                  color='primary'
                  onClick={submitForm}
                >
                  {t('Save')}
                </Button>
              </Box>
            </PageHeader>
            <Stepper activeStep={step}>
              <Step>
                <StepButton onClick={() => setStep(0)}>
                  {t('Details')}
                </StepButton>
              </Step>
              <Step>
                <StepButton onClick={() => setStep(1)}>
                  {t('Programme Partners')}
                </StepButton>
              </Step>
            </Stepper>
            {step === 0 && (
              <DetailsStep values={values} step={step} setStep={setStep} />
            )}
            {step === 1 && (
              <PartnersStep values={values} allAreasTree={allAreasTree} />
            )}
          </>
        );
      }}
    </Formik>
  );
};
