import React, { useState } from 'react';
import styled from 'styled-components';
import {
  Button,
  DialogContent,
  DialogTitle,
  TextField,
  Typography,
} from '@material-ui/core';
import CheckRoundedIcon from '@material-ui/icons/CheckRounded';
import {
  RegistrationDetailedFragment,
  useApproveRdiMutation,
} from '../../../__generated__/graphql';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { Dialog } from '../../dialogs/Dialog';
import { DialogActions } from '../../dialogs/DialogActions';

const DialogTitleWrapper = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
`;

const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;

const DialogDescription = styled.div`
  margin: 20px 0;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
`;

interface ApproveRegistrationDataImportDialogProps {
  registration: RegistrationDetailedFragment;
}

export function ApproveRegistrationDataImportDialog({
  registration,
}: ApproveRegistrationDataImportDialogProps): React.ReactElement {
  const [open, setOpen] = useState(false);
  const { showMessage } = useSnackbar();
  const [mutate] = useApproveRdiMutation({
    variables: { id: registration.id },
  });
  const approve = async (): Promise<void> => {
    const { errors } = await mutate();
    if (errors) {
      showMessage('Error while approving Registration Data Import');
      return;
    }
    showMessage('Registration Data Import Approved');
  };
  return (
    <span>
      <Button
        startIcon={<CheckRoundedIcon />}
        color='primary'
        variant='contained'
        onClick={() => setOpen(true)}
        data-cy='button-approve'
      >
        Approve
      </Button>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        scroll='paper'
        aria-labelledby='form-dialog-title'
      >
        <DialogTitleWrapper>
          <DialogTitle id='scroll-dialog-title'>
            <Typography variant='h6'>Approve Import</Typography>
          </DialogTitle>
        </DialogTitleWrapper>
        <DialogContent>
          <DialogDescription>
            <div>Are your sure you want to approve this data import?</div>
            <div>
              <strong>{registration.numberOfHouseholds} households and {registration.numberOfIndividuals} individuals will be approved. </strong>
              Do you want to proceed?
            </div>
          </DialogDescription>
        </DialogContent>
        <DialogFooter>
          <DialogActions>
            <Button onClick={() => setOpen(false)}>CANCEL</Button>
            <Button
              type='submit'
              color='primary'
              variant='contained'
              onClick={approve}
              data-cy='button-approve'
            >
              APPROVE
            </Button>
          </DialogActions>
        </DialogFooter>
      </Dialog>
    </span>
  );
}
