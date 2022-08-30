import {
  Box,
  Button,
  FormHelperText,
  Grid,
  GridSize,
  Step,
  StepLabel,
  Stepper,
  Typography,
} from '@material-ui/core';
import { Field, Formik } from 'formik';
import React, { ReactElement, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useHistory } from 'react-router-dom';
import styled from 'styled-components';
import {
  hasPermissionInModule,
  hasPermissions,
  PERMISSIONS,
} from '../../../config/permissions';
import { useArrayToDict } from '../../../hooks/useArrayToDict';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { usePermissions } from '../../../hooks/usePermissions';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { FormikAdminAreaAutocomplete } from '../../../shared/Formik/FormikAdminAreaAutocomplete';
import { FormikCheckboxField } from '../../../shared/Formik/FormikCheckboxField';
import { FormikSelectField } from '../../../shared/Formik/FormikSelectField';
import { FormikTextField } from '../../../shared/Formik/FormikTextField';
import {
  GrievanceSteps,
  GRIEVANCE_CATEGORIES,
  GRIEVANCE_ISSUE_TYPES,
  GRIEVANCE_SUB_CATEGORIES,
} from '../../../utils/constants';
import {
  isInvalid,
  reduceChoices,
  thingForSpecificGrievanceType,
} from '../../../utils/utils';
import {
  useAllAddIndividualFieldsQuery,
  useAllEditHouseholdFieldsQuery,
  useAllProgramsQuery,
  useAllUsersQuery,
  useCreateGrievanceMutation,
  useGrievancesChoiceDataQuery,
  useUserChoiceDataQuery,
} from '../../../__generated__/graphql';
import { BreadCrumbsItem } from '../../../components/core/BreadCrumbs';
import { ContainerColumnWithBorder } from '../../../components/core/ContainerColumnWithBorder';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { PageHeader } from '../../../components/core/PageHeader';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { AddIndividualDataChange } from '../../../components/grievances/AddIndividualDataChange';
import { Consent } from '../../../components/grievances/Consent';
import { EditHouseholdDataChange } from '../../../components/grievances/EditHouseholdDataChange/EditHouseholdDataChange';
import { EditIndividualDataChange } from '../../../components/grievances/EditIndividualDataChange/EditIndividualDataChange';
import { OtherRelatedTicketsCreate } from '../../../components/grievances/OtherRelatedTicketsCreate';
import { TicketsAlreadyExist } from '../../../components/grievances/TicketsAlreadyExist';
import { prepareVariables } from '../../../components/grievances/utils/createGrievanceUtils';
import { validateUsingSteps } from '../../../components/grievances/utils/validateGrievance';
import { validationSchemaWithSteps } from '../../../components/grievances/utils/validationSchema';
import { LoadingButton } from '../../../components/core/LoadingButton';
import { LabelizedField } from '../../../components/core/LabelizedField';
import { OverviewContainer } from '../../../components/core/OverviewContainer';
import { ContentLink } from '../../../components/core/ContentLink';
import { LookUpRelatedTickets } from '../../../components/grievances/LookUps/LookUpRelatedTickets/LookUpRelatedTickets';
import { LookUpHouseholdIndividualSelection } from '../../../components/grievances/LookUps/LookUpHouseholdIndividual/LookUpHouseholdIndividualSelection';

const steps = [
  'Category Selection',
  'Household/Individual Look up',
  'Identity Verification',
  'Description',
];

const BoxPadding = styled.div`
  padding: 15px 0;
`;
const NoRootPadding = styled.div`
  .MuiStepper-root {
    padding: 0 !important;
  }
`;
const InnerBoxPadding = styled.div`
  .MuiPaper-root {
    padding: 32px 20px;
  }
`;
const NewTicket = styled.div`
  padding: 20px;
`;
const BoxWithBorderBottom = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  padding: 15px 0;
`;
const BoxWithBorders = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  padding: 15px 0;
`;
const EmptyComponent = (): React.ReactElement => null;
export const dataChangeComponentDict = {
  [GRIEVANCE_CATEGORIES.DATA_CHANGE]: {
    [GRIEVANCE_ISSUE_TYPES.ADD_INDIVIDUAL]: AddIndividualDataChange,
    [GRIEVANCE_ISSUE_TYPES.EDIT_INDIVIDUAL]: EditIndividualDataChange,
    [GRIEVANCE_ISSUE_TYPES.EDIT_HOUSEHOLD]: EditHouseholdDataChange,
  },
};

export const CreateGrievancePage = (): React.ReactElement => {
  const { t } = useTranslation();
  const history = useHistory();
  const businessArea = useBusinessArea();
  const permissions = usePermissions();
  const { showMessage } = useSnackbar();

  const [activeStep, setActiveStep] = useState(GrievanceSteps.Selection);

  const linkedTicketId = history.location.state?.linkedTicketId;
  const selectedHousehold = history.location.state?.selectedHousehold;
  const selectedIndividual = history.location.state?.selectedIndividual;
  const category = history.location.state?.category;

  const initialValues = {
    description: '',
    category: category || null,
    language: '',
    consent: false,
    admin: null,
    area: '',
    selectedHousehold: selectedHousehold || null,
    selectedIndividual: selectedIndividual || null,
    selectedPaymentRecords: [],
    selectedRelatedTickets: linkedTicketId ? [linkedTicketId] : [],
    identityVerified: false,
    issueType: null,
    priority: 3,
    urgency: 3,
    subCategory: null,
    partner: null,
    programme: null,
    comments: null,
  };
  const { data: userData, loading: userDataLoading } = useAllUsersQuery({
    variables: { businessArea, first: 1000 },
  });

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useGrievancesChoiceDataQuery();

  const priorityChoicesData = choicesData.grievanceTicketPriorityChoices;
  const urgencyChoicesData = choicesData.grievanceTicketUrgencyChoices;
  const categoryChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketCategoryChoices);

  const mappedPriorities = Array.from(Array(3).keys()).map((i) => ({
    name: priorityChoicesData[i]?.name,
    value: i + 1,
  }));

  const { data: userChoices } = useUserChoiceDataQuery();

  const mappedUrgencies = Array.from(Array(3).keys()).map((i) => ({
    name: urgencyChoicesData[i]?.name,
    value: i + 1,
  }));

  const [mutate, { loading }] = useCreateGrievanceMutation();
  const {
    data: allAddIndividualFieldsData,
    loading: allAddIndividualFieldsDataLoading,
  } = useAllAddIndividualFieldsQuery();
  const {
    data: householdFieldsData,
    loading: householdFieldsLoading,
  } = useAllEditHouseholdFieldsQuery();
  const individualFieldsDict = useArrayToDict(
    allAddIndividualFieldsData?.allAddIndividualsFieldsAttributes,
    'name',
    '*',
  );
  const householdFieldsDict = useArrayToDict(
    householdFieldsData?.allEditHouseholdFieldsAttributes,
    'name',
    '*',
  );
  const issueTypeDict = useArrayToDict(
    choicesData?.grievanceTicketIssueTypeChoices,
    'category',
    '*',
  );

  const {
    data: allProgramsData,
    loading: loadingPrograms,
  } = useAllProgramsQuery({
    variables: { businessArea, status: ['ACTIVE'] },
    fetchPolicy: 'cache-and-network',
  });

  const allProgramsEdges = allProgramsData?.allPrograms?.edges || [];
  const mappedPrograms = allProgramsEdges.map((edge) => ({
    name: edge.node?.name,
    value: edge.node.id,
  }));

  const showSubCategory = (values): boolean => {
    return values.category === GRIEVANCE_CATEGORIES.GRIEVANCE_COMPLAINT;
  };
  const showIssueType = (values): boolean => {
    return (
      values.category === GRIEVANCE_CATEGORIES.SENSITIVE_GRIEVANCE ||
      values.category === GRIEVANCE_CATEGORIES.DATA_CHANGE
    );
  };

  const subCategoryChoices: {
    [id: number]: string;
  } = reduceChoices(choicesData.grievanceTicketSubCategoryChoices);

  if (
    userDataLoading ||
    choicesLoading ||
    allAddIndividualFieldsDataLoading ||
    householdFieldsLoading ||
    loadingPrograms
  )
    return <LoadingComponent />;
  if (permissions === null) return null;

  if (!hasPermissions(PERMISSIONS.GRIEVANCES_CREATE, permissions))
    return <PermissionDenied />;

  if (
    !choicesData ||
    !userData ||
    !allAddIndividualFieldsData ||
    !householdFieldsData ||
    !householdFieldsDict ||
    !individualFieldsDict
  )
    return null;

  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: t('Grievance and Feedback'),
      to: `/${businessArea}/grievance-and-feedback/tickets/`,
    },
  ];

  const dataChangeErrors = (errors, touched): ReactElement[] =>
    [
      'householdDataUpdateFields',
      'individualDataUpdateFields',
      'individualDataUpdateFieldsDocuments',
      'individualDataUpdateFieldsIdentities',
      'verificationRequired',
    ]
      .filter(
        (fieldname) =>
          isInvalid(fieldname, errors, touched) ||
          fieldname === 'verificationRequired',
      )
      .map((fieldname) => (
        <FormHelperText key={fieldname} error>
          {errors[fieldname]}
        </FormHelperText>
      ));

  const hasCategorySelected = (values): boolean => {
    return !!values.category;
  };

  const hasHouseholdSelected = (values): boolean => {
    return !!values.selectedHousehold?.id;
  };

  const hasIndividualSelected = (values): boolean => {
    return !!values.selectedIndividual?.id;
  };

  const renderAlreadyExistsBox = (values): ReactElement => {
    if (
      hasCategorySelected(values) &&
      (hasHouseholdSelected(values) || hasIndividualSelected(values))
    ) {
      return <TicketsAlreadyExist values={values} />;
    }
    return null;
  };

  const handleNext = (): void => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = (): void => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const selectedIssueType = (values): string => {
    return values.issueType
      ? choicesData.grievanceTicketIssueTypeChoices
          .filter((el) => el.category === values.category.toString())[0]
          .subCategories.filter(
            (el) => el.value === values.issueType.toString(),
          )[0].name
      : '-';
  };

  const showHouseholdQuestionnaire = (values): ReactElement => {
    const selectedHouseholdData = values.selectedHousehold;
    return (
      <Grid container spacing={6}>
        {[
          {
            name: 'size',
            label: t('Household Size'),
            value: selectedHouseholdData.size,
            size: 3,
          },
          {
            name: 'maleChildrenCount',
            label: t('Number of Male Children'),
            value: selectedHouseholdData.maleChildrenCount?.toString(),
            size: 3,
          },
          {
            name: 'femaleChildrenCount',
            label: t('Number of Female Children'),
            value: selectedHouseholdData.femaleChildrenCount?.toString(),
            size: 3,
          },
          {
            name: 'childrenDisabledCount',
            label: t('Number of Disabled Children'),
            value: selectedHouseholdData.childrenDisabledCount?.toString(),
            size: 3,
          },
          {
            name: 'headOfHousehold',
            label: t('Head of Household'),
            value: (
              <ContentLink
                href={`/${businessArea}/population/individuals/${selectedHouseholdData.headOfHousehold.id}`}
              >
                {selectedHouseholdData.headOfHousehold.fullName}
              </ContentLink>
            ),
            size: 3,
          },
          {
            name: 'countryOrigin',
            label: t('Country of Origin'),
            value: selectedHouseholdData.countryOrigin,
            size: 3,
          },
          {
            name: 'address',
            label: t('Address'),
            value: selectedHouseholdData.address,
            size: 3,
          },
          {
            name: 'village',
            label: t('Village'),
            value: selectedHouseholdData.village,
            size: 3,
          },
          {
            name: 'admin1',
            label: t('Administrative Level 1'),
            value: selectedHouseholdData.admin1?.name,
            size: 3,
          },
          {
            name: 'unhcrId',
            label: t('UNHCR CASE ID'),
            value: selectedHouseholdData.unicefId,
            size: 3,
          },
          {
            name: 'months_displaced_h_f',
            label: t('LENGTH OF TIME SINCE ARRIVAL'),
            value: selectedHouseholdData.flexFields?.months_displaced_h_f,
            size: 3,
          },
        ].map((el) => (
          <Grid item xs={3}>
            <Field
              name={el.name}
              label={el.label}
              displayValue={el.value || '-'}
              color='primary'
              component={FormikCheckboxField}
            />
          </Grid>
        ))}
      </Grid>
    );
  };

  const showIndividualQuestionnaire = (values): ReactElement => {
    const selectedIndividualData =
      values.selectedIndividual || values.selectedHousehold.headOfHousehold;
    return (
      <Grid container spacing={6}>
        {[
          {
            name: 'fullName',
            label: t('Individual Full Name'),
            value: (
              <ContentLink
                href={`/${businessArea}/population/individuals/${selectedIndividualData.id}`}
              >
                {selectedIndividualData.fullName}
              </ContentLink>
            ),
            size: 3,
          },
          {
            name: 'birthDate',
            label: t('Birth Date'),
            value: selectedIndividualData.birthDate,
            size: 3,
          },
          {
            name: 'phoneNo',
            label: t('Phone Number'),
            value: selectedIndividualData.phoneNo,
            size: 3,
          },
          {
            name: 'relationship',
            label: t('Relationship to HOH'),
            value: selectedIndividualData.relationship,
            size: 3,
          },
        ].map((el) => (
          <Grid item xs={3}>
            <Field
              name={el.name}
              label={el.label}
              displayValue={el.value || '-'}
              color='primary'
              component={FormikCheckboxField}
            />
          </Grid>
        ))}
      </Grid>
    );
  };

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={async (values) => {
        if (activeStep === steps.length - 1) {
          try {
            const response = await mutate(
              prepareVariables(businessArea, values),
            );
            if (values.selectedPaymentRecords.length > 1) {
              showMessage(
                `${values.selectedPaymentRecords.length} ${t(
                  'Grievance Tickets created',
                )}.`,
                {
                  pathname: `/${businessArea}/grievance-and-feedback`,
                  historyMethod: 'push',
                },
              );
            } else {
              showMessage(t('Grievance Ticket created.'), {
                pathname: `/${businessArea}/grievance-and-feedback/${response.data.createGrievanceTicket.grievanceTickets[0].id}`,
                historyMethod: 'push',
              });
            }
          } catch (e) {
            e.graphQLErrors.map((x) => showMessage(x.message));
          }
        } else {
          handleNext();
        }
      }}
      validate={(values) =>
        validateUsingSteps(
          values,
          allAddIndividualFieldsData,
          individualFieldsDict,
          householdFieldsDict,
          activeStep,
        )
      }
      validationSchema={validationSchemaWithSteps(activeStep)}
    >
      {({ submitForm, values, setFieldValue, errors, touched }) => {
        const DataChangeComponent = thingForSpecificGrievanceType(
          values,
          dataChangeComponentDict,
          EmptyComponent,
        );
        return (
          <>
            <PageHeader
              title='New Ticket'
              breadCrumbs={
                hasPermissionInModule('GRIEVANCES_VIEW_LIST', permissions)
                  ? breadCrumbsItems
                  : null
              }
            />
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <NewTicket>
                  <InnerBoxPadding>
                    <ContainerColumnWithBorder>
                      <NoRootPadding>
                        <Stepper activeStep={activeStep}>
                          {steps.map((label) => {
                            const stepProps: { completed?: boolean } = {};
                            const labelProps: {
                              optional?: React.ReactNode;
                            } = {};
                            return (
                              <Step key={label} {...stepProps}>
                                <StepLabel {...labelProps}>{label}</StepLabel>
                              </Step>
                            );
                          })}
                        </Stepper>
                      </NoRootPadding>
                      {activeStep === GrievanceSteps.Selection && (
                        <Grid container spacing={3}>
                          <Grid item xs={6}>
                            <Field
                              name='category'
                              label='Category*'
                              onChange={(e) => {
                                setFieldValue('category', e.target.value);
                                setFieldValue('issueType', null);
                                setFieldValue('subCategory', null);
                              }}
                              variant='outlined'
                              choices={
                                choicesData.grievanceTicketManualCategoryChoices
                              }
                              component={FormikSelectField}
                            />
                          </Grid>
                          {showIssueType(values) && (
                            <Grid item xs={6}>
                              <Field
                                name='issueType'
                                label='Issue Type*'
                                variant='outlined'
                                choices={
                                  issueTypeDict[values.category].subCategories
                                }
                                component={FormikSelectField}
                              />
                            </Grid>
                          )}
                          {showSubCategory(values) && (
                            <Grid item xs={6}>
                              <Field
                                name='subCategory'
                                label={t('Issue Type')}
                                onChange={(e) => {
                                  setFieldValue('subCategory', e.target.value);
                                }}
                                variant='outlined'
                                choices={
                                  choicesData.grievanceTicketSubCategoryChoices
                                }
                                component={FormikSelectField}
                              />
                            </Grid>
                          )}
                        </Grid>
                      )}
                      {activeStep === GrievanceSteps.Lookup && (
                        <BoxWithBorders>
                          <Box display='flex' flexDirection='column'>
                            <LookUpHouseholdIndividualSelection
                              values={values}
                              onValueChange={setFieldValue}
                              errors={errors}
                              touched={touched}
                            />
                          </Box>
                        </BoxWithBorders>
                      )}
                      {activeStep === GrievanceSteps.Verification && (
                        <BoxWithBorders>
                          {values.selectedHousehold && (
                            <>
                              <Typography variant='subtitle1'>
                                {t(
                                  'Select correctly answered questions (minimum 5)',
                                )}
                              </Typography>
                              <Box py={4}>
                                <Typography variant='subtitle2'>
                                  {t('Household Questionnaire')}
                                </Typography>
                                <Box py={4}>
                                  {showHouseholdQuestionnaire(values)}
                                </Box>
                              </Box>
                              <Typography variant='subtitle2'>
                                {t('Individual Questionnaire')}
                              </Typography>
                              <Box py={4}>
                                {showIndividualQuestionnaire(values)}
                              </Box>
                              <BoxWithBorderBottom />
                            </>
                          )}
                          <Consent />
                          <Field
                            name='consent'
                            label={t('Received Consent*')}
                            color='primary'
                            fullWidth
                            container={false}
                            component={FormikCheckboxField}
                          />
                        </BoxWithBorders>
                      )}
                      {activeStep === steps.length - 1 && (
                        <BoxPadding>
                          <OverviewContainer>
                            <Grid container spacing={6}>
                              {[
                                {
                                  label: t('Category'),
                                  value: (
                                    <span>
                                      {categoryChoices[values.category]}
                                    </span>
                                  ),
                                  size: 3,
                                },
                                showIssueType(values) && {
                                  label: t('Issue Type'),
                                  value: (
                                    <span>{selectedIssueType(values)}</span>
                                  ),
                                  size: 9,
                                },
                                showSubCategory(values) && {
                                  label: t('Issue Type'),
                                  value: (
                                    <span>
                                      {subCategoryChoices[values.subCategory] ||
                                        '-'}
                                    </span>
                                  ),
                                  size: 9,
                                },
                                {
                                  label: t('HOUSEHOLD ID'),
                                  value: (
                                    <span>
                                      {values.selectedHousehold?.id ? (
                                        <ContentLink
                                          href={`/${businessArea}/population/household/${values.selectedHousehold.id}`}
                                        >
                                          {values.selectedHousehold.unicefId}
                                        </ContentLink>
                                      ) : (
                                        '-'
                                      )}
                                    </span>
                                  ),
                                  size: 3,
                                },
                                {
                                  label: t('INDIVIDUAL ID'),
                                  value: (
                                    <span>
                                      {values.selectedIndividual?.id ? (
                                        <ContentLink
                                          href={`/${businessArea}/population/individuals/${values.selectedIndividual.id}`}
                                        >
                                          {values.selectedIndividual.unicefId}
                                        </ContentLink>
                                      ) : (
                                        '-'
                                      )}
                                    </span>
                                  ),
                                  size: 3,
                                },
                              ]
                                .filter((el) => el)
                                .map((el) => (
                                  <Grid
                                    key={el.label}
                                    item
                                    xs={el.size as GridSize}
                                  >
                                    <LabelizedField label={el.label}>
                                      {el.value}
                                    </LabelizedField>
                                  </Grid>
                                ))}
                            </Grid>
                          </OverviewContainer>
                          <BoxWithBorderBottom />
                          <BoxPadding />
                          <Grid container spacing={3}>
                            {values.subCategory ===
                              GRIEVANCE_SUB_CATEGORIES.PARTNER_COMPLAINT && (
                              <Grid item xs={3}>
                                <Field
                                  name='partner'
                                  fullWidth
                                  variant='outlined'
                                  label={t('Partner')}
                                  choices={userChoices.userPartnerChoices}
                                  component={FormikSelectField}
                                />
                              </Grid>
                            )}
                            <Grid item xs={12}>
                              <Field
                                name='description'
                                multiline
                                fullWidth
                                variant='outlined'
                                label='Description*'
                                component={FormikTextField}
                              />
                            </Grid>
                            <Grid item xs={12}>
                              <Field
                                name='comments'
                                multiline
                                fullWidth
                                variant='outlined'
                                label='Comments'
                                component={FormikTextField}
                              />
                            </Grid>
                            <Grid item xs={6}>
                              <Field
                                name='admin'
                                label={t('Administrative Level 2')}
                                variant='outlined'
                                component={FormikAdminAreaAutocomplete}
                              />
                            </Grid>
                            <Grid item xs={6}>
                              <Field
                                name='area'
                                fullWidth
                                variant='outlined'
                                label={t('Area / Village / Pay point')}
                                component={FormikTextField}
                              />
                            </Grid>
                            <Grid item xs={6}>
                              <Field
                                name='language'
                                multiline
                                fullWidth
                                variant='outlined'
                                label={t('Languages Spoken')}
                                component={FormikTextField}
                              />
                            </Grid>
                            <Grid item xs={3}>
                              <Field
                                name='priority'
                                multiline
                                fullWidth
                                variant='outlined'
                                label={t('Priority')}
                                choices={mappedPriorities}
                                component={FormikSelectField}
                              />
                            </Grid>
                            <Grid item xs={3}>
                              <Field
                                name='urgency'
                                multiline
                                fullWidth
                                variant='outlined'
                                label={t('Urgency')}
                                choices={mappedUrgencies}
                                component={FormikSelectField}
                              />
                            </Grid>
                            {+values.issueType !==
                              +GRIEVANCE_ISSUE_TYPES.ADD_INDIVIDUAL && (
                              <Grid item xs={6}>
                                <Field
                                  name='programme'
                                  fullWidth
                                  variant='outlined'
                                  label={t('Programme')}
                                  choices={mappedPrograms}
                                  component={FormikSelectField}
                                />
                              </Grid>
                            )}
                          </Grid>
                          <Box pt={5}>
                            <BoxWithBorders>
                              <Grid item xs={6}>
                                <Box py={3}>
                                  <LookUpRelatedTickets
                                    values={values}
                                    onValueChange={setFieldValue}
                                  />
                                </Box>
                              </Grid>
                            </BoxWithBorders>
                          </Box>
                        </BoxPadding>
                      )}
                      {activeStep === steps.length - 1 && (
                        <DataChangeComponent
                          values={values}
                          setFieldValue={setFieldValue}
                        />
                      )}
                      {dataChangeErrors(errors, touched)}
                      <Box pt={3} display='flex' flexDirection='row'>
                        <Box mr={3}>
                          <Button
                            component={Link}
                            to={`/${businessArea}/grievance-and-feedback/tickets`}
                          >
                            {t('Cancel')}
                          </Button>
                        </Box>
                        <Box display='flex' ml='auto'>
                          <Button
                            disabled={activeStep === 0}
                            onClick={handleBack}
                          >
                            {t('Back')}
                          </Button>
                          <LoadingButton
                            loading={loading}
                            color='primary'
                            variant='contained'
                            onClick={submitForm}
                          >
                            {activeStep === steps.length - 1
                              ? t('Save')
                              : t('Next')}
                          </LoadingButton>
                        </Box>
                      </Box>
                    </ContainerColumnWithBorder>
                  </InnerBoxPadding>
                </NewTicket>
              </Grid>
              {activeStep === steps.length - 1 && (
                <Grid item xs={12}>
                  <NewTicket>
                    <Grid container spacing={3}>
                      <Grid item xs={6}>
                        {renderAlreadyExistsBox(values)}
                      </Grid>
                      <Grid item xs={6}>
                        {values.category && values.selectedHousehold?.id && (
                          <OtherRelatedTicketsCreate values={values} />
                        )}
                      </Grid>
                    </Grid>
                  </NewTicket>
                </Grid>
              )}
            </Grid>
          </>
        );
      }}
    </Formik>
  );
};
