import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle, TextField,
  Typography,
} from '@material-ui/core';
import React, { FC } from 'react';
import { useTranslation } from 'react-i18next';
import { DialogFooter } from '../../../containers/dialogs/DialogFooter';
import { DialogTitleWrapper } from '../../../containers/dialogs/DialogTitleWrapper';

export interface TextAreaOptions {
  title: string,
  maxLength: number
}

export interface ConfirmationDialogOptions {
  catchOnCancel?: boolean;
  title?: string;
  content?: string | React.ReactElement;
  continueText?: string;
  extraContent?: string;
  warningContent?: string | null;
  disabled?: boolean;
  textArea?: TextAreaOptions
}

export interface ConfirmationDialogProps extends ConfirmationDialogOptions {
  open: boolean;
  onSubmit: () => void;
  onClose: () => void;
}

export const ConfirmationDialog: FC<ConfirmationDialogProps> = ({
  open,
  title,
  content,
  continueText,
  extraContent,
  warningContent,
  onSubmit,
  onClose,
  disabled = false,
  textArea
}) => {
  const { t } = useTranslation();

  return (
    <Dialog fullWidth scroll='paper' open={open}>
      <DialogTitleWrapper>
        <DialogTitle>{title || t('Confirmation')}</DialogTitle>
      </DialogTitleWrapper>
      <DialogContent>
        {extraContent ? (
          <Typography variant='body2' style={{ marginBottom: '16px' }}>
            {extraContent}
          </Typography>
        ) : null}
        <Typography
          variant='body2'
          style={{ marginBottom: warningContent ? '16px' : 'inherit' }}
        >
          {content}
        </Typography>
        {warningContent ? (
          <Typography
            color='primary'
            variant='body2'
            style={{ fontWeight: 'bold' }}
          >
            {warningContent}
          </Typography>
        ) : null}
        {textArea ? (
            <TextField
              multiline
              fullWidth
              required
              id="outlined-multiline-static"
              label={textArea.title}
              rows={3}
              variant="filled"
              style={{ marginTop: "10px", marginBottom: "10px" }}
              inputProps={{ maxLength: textArea.maxLength }}
            />
        ) : null}
      </DialogContent>
      <DialogFooter>
        <DialogActions>
          <Button
            data-cy='button-cancel'
            color='primary'
            onClick={onClose}
            autoFocus
          >
            {t('Cancel')}
          </Button>
          <Button
            variant='contained'
            color='primary'
            disabled={disabled}
            onClick={onSubmit}
            data-cy='button-confirm'
          >
            {continueText || t('Continue')}
          </Button>
        </DialogActions>
      </DialogFooter>
    </Dialog>
  );
};
