import { Button, DialogContent, DialogTitle } from '@material-ui/core';
import { Field, Formik } from 'formik';
import React from 'react';
import { useTranslation } from 'react-i18next';
import * as Yup from 'yup';
import { useHistory } from 'react-router-dom';
import { AutoSubmitFormOnEnter } from '../../../components/core/AutoSubmitFormOnEnter';
import { LoadingButton } from '../../../components/core/LoadingButton';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { FormikTextField } from '../../../shared/Formik/FormikTextField';
import { useCopyTargetPopulationMutation } from '../../../__generated__/graphql';
import { Dialog } from '../Dialog';
import { DialogActions } from '../DialogActions';
import { DialogDescription } from '../DialogDescription';
import { DialogFooter } from '../DialogFooter';
import { DialogTitleWrapper } from '../DialogTitleWrapper';
import { useBaseUrl } from '../../../hooks/useBaseUrl';

export interface FinalizeTargetPopulationPropTypes {
  open: boolean;
  setOpen: Function;
}

const validationSchema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
});

interface DuplicateTargetPopulationPropTypes {
  open: boolean;
  setOpen: Function;
  targetPopulationId: string;
}

export const DuplicateTargetPopulation = ({
  open,
  setOpen,
  targetPopulationId,
}: DuplicateTargetPopulationPropTypes): React.ReactElement => {
  const history = useHistory();
  const { t } = useTranslation();
  const [mutate, { loading }] = useCopyTargetPopulationMutation();
  const { showMessage } = useSnackbar();
  const { baseUrl } = useBaseUrl();
  const initialValues = {
    name: '',
    id: targetPopulationId,
  };

  return (
    <Dialog
      open={open}
      onClose={() => setOpen(false)}
      scroll='paper'
      aria-labelledby='form-dialog-title'
    >
      <Formik
        validationSchema={validationSchema}
        initialValues={initialValues}
        onSubmit={async (values) => {
          try {
            const res = await mutate({
              variables: { input: { targetPopulationData: { ...values } } },
            });
            setOpen(false);
            showMessage(t('Target Population Duplicated'));
            history.push(
              `/${baseUrl}/target-population/${res.data.copyTargetPopulation.targetPopulation.id}`,
            );
          } catch (e) {
            e.graphQLErrors.map((x) => showMessage(x.message));
          }
        }}
      >
        {({ submitForm }) => (
          <>
            {open && <AutoSubmitFormOnEnter />}
            <DialogTitleWrapper>
              <DialogTitle>Duplicate Target Population?</DialogTitle>
            </DialogTitleWrapper>
            <DialogContent>
              <DialogDescription>
                {t(
                  'Please use a unique name for the copy of this Target Population.',
                )}
                <br /> <strong>{t('Note')}</strong>:{' '}
                {t(
                  'This duplicate will copy the Target Criteria of the Programme Population and update to the latest results from the system.',
                )}
              </DialogDescription>
              <Field
                name='name'
                fullWidth
                label={t('Name Copy of Target Population')}
                required
                variant='outlined'
                component={FormikTextField}
              />
            </DialogContent>
            <DialogFooter>
              <DialogActions>
                <Button data-cy='button-cancel' onClick={() => setOpen(false)}>
                  {t('CANCEL')}
                </Button>
                <LoadingButton
                  loading={loading}
                  type='submit'
                  color='primary'
                  variant='contained'
                  onClick={submitForm}
                  data-cy='button-target-population-duplicate'
                >
                  {t('Save')}
                </LoadingButton>
              </DialogActions>
            </DialogFooter>
          </>
        )}
      </Formik>
    </Dialog>
  );
};
