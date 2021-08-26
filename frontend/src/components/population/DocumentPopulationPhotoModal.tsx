import { Box, Button, DialogContent, DialogTitle } from '@material-ui/core';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { Dialog } from '../../containers/dialogs/Dialog';
import { DialogActions } from '../../containers/dialogs/DialogActions';
import {
  IndividualNode,
  useIndividualPhotosLazyQuery,
} from '../../__generated__/graphql';
import { BlackLink } from '../BlackLink';

const DialogTitleWrapper = styled.div`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
`;

const DialogFooter = styled.div`
  padding: 12px 16px;
  margin: 0;
  border-top: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  text-align: right;
`;

const StyledImage = styled.img`
  max-width: 100%;
  max-height: 100%;
`;

interface DocumentPopulationPhotoModalProps {
  individual: IndividualNode;
  documentNumber: string;
  documentId: string;
}

export const DocumentPopulationPhotoModal = ({
  individual,
  documentNumber,
  documentId,
}: DocumentPopulationPhotoModalProps): React.ReactElement => {
  const { t } = useTranslation();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [getPhotos, { data }] = useIndividualPhotosLazyQuery({
    variables: { id: individual?.id },
    fetchPolicy: 'network-only',
  });
  const documentWithPhoto = data?.individual?.documents?.edges?.find(
    (el) => el.node.id === documentId,
  );

  return (
    <>
      <BlackLink
        onClick={() => {
          setDialogOpen(true);
          getPhotos();
        }}
      >
        {documentNumber}
      </BlackLink>
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        aria-labelledby='form-dialog-title'
      >
        <DialogTitleWrapper>
          <DialogTitle id='scroll-dialog-title'>
            Document&apos;s Photo
          </DialogTitle>
        </DialogTitleWrapper>
        <DialogContent>
          <Box p={3}>
            <StyledImage alt='document' src={documentWithPhoto?.node?.photo} />
          </Box>
        </DialogContent>
        <DialogFooter>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>{t('CANCEL')}</Button>
          </DialogActions>
        </DialogFooter>
      </Dialog>
    </>
  );
};
