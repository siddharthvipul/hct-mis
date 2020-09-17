import React, { useState, ReactElement } from 'react';
import { Button } from '@material-ui/core';
import { useCreateProgramMutation } from '../../../__generated__/graphql';
import { ProgramForm } from '../../forms/ProgramForm';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { ALL_PROGRAMS_QUERY } from '../../../apollo/queries/AllPrograms';
import { UniversalMoment } from '../../../components/UniversalMoment';

export function CreateProgram(): ReactElement {
  const [open, setOpen] = useState(false);
  const { showMessage } = useSnackbar();
  const [mutate] = useCreateProgramMutation();
  const businessArea = useBusinessArea();

  const submitFormHandler = async (values): Promise<void> => {
    const response = await mutate({
      variables: {
        programData: {
          ...values,
          startDate: <UniversalMoment>{values.startDate}</UniversalMoment>,
          endDate: <UniversalMoment>{values.endDate}</UniversalMoment>,
          businessAreaSlug: businessArea,
        },
      },
      refetchQueries: () => [{ query: ALL_PROGRAMS_QUERY }],
    });
    if (!response.errors && response.data.createProgram) {
      showMessage('Programme created.', {
        pathname: `/${businessArea}/programs/${response.data.createProgram.program.id}`,
        historyMethod: 'push',
      });
    } else {
      showMessage('Programme create action failed.');
    }
  };

  const renderSubmit = (submit): ReactElement => {
    return (
      <>
        <Button onClick={() => setOpen(false)}>Cancel</Button>
        <Button
          onClick={submit}
          type='submit'
          color='primary'
          variant='contained'
          data-cy='button-save'
        >
          Save
        </Button>
      </>
    );
  };

  return (
    <div>
      <Button
        variant='contained'
        color='primary'
        onClick={() => setOpen(true)}
        data-cy='button-new-program'
      >
        new programme
      </Button>

      <ProgramForm
        onSubmit={submitFormHandler}
        renderSubmit={renderSubmit}
        open={open}
        onClose={() => setOpen(false)}
        title='Set-up a new Programme'
      />
    </div>
  );
}
