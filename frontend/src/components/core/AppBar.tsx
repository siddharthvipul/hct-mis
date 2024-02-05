import { Box, Button, makeStyles } from '@mui/material';
import MuiAppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton';
import Toolbar from '@mui/material/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import TextsmsIcon from '@material-ui/icons/Textsms';
import clsx from 'clsx';
import React from 'react';
import styled from 'styled-components';
import { BusinessAreaSelect } from '../../containers/BusinessAreaSelect';
import { GlobalProgramSelect } from '../../containers/GlobalProgramSelect';
import { UserProfileMenu } from '../../containers/UserProfileMenu';
import { useCachedMe } from '../../hooks/useCachedMe';
import { MiśTheme } from '../../theme';

const useStyles = makeStyles((theme: MiśTheme) => ({
  root: {
    display: 'flex',
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    position: 'fixed',
    top: 0,
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: theme.palette.secondary.main,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: theme.drawer.width,
    width: `calc(100% - ${theme.drawer.width}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  appBarSpacer: theme.mixins.toolbar,
}));

const StyledToolbar = styled(Toolbar)`
  display: flex;
  justify-content: space-between;
`;
const StyledLink = styled.a`
  text-decoration: none;
  color: #e3e6e7;
`;

export const AppBar = ({ open, handleDrawerOpen }): React.ReactElement => {
  const { data: meData, loading: meLoading } = useCachedMe();
  const classes = useStyles({});
  const servicenow = `https://unicef.service-now.com/cc?id=sc_cat_item&sys_id=762ae3128747d91021cb670a0cbb35a7&HOPE - ${
    window.location.pathname.split('/')[2]
  }&Workspace: ${window.location.pathname.split('/')[1]} \n Url: ${
    window.location.href
  }`;

  if (meLoading) {
    return null;
  }
  return (
    <MuiAppBar className={clsx(classes.appBar, open && classes.appBarShift)}>
      <StyledToolbar>
        <Box display="flex" alignItems="center" justifyContent="center">
          <Box ml={1}>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              className={clsx(
                classes.menuButton,
                open && classes.menuButtonHidden,
              )}
            >
              <MenuIcon />
            </IconButton>
          </Box>
          <Box display="flex" alignItems="center">
            <Box ml={6} data-cy="business-area-container">
              <BusinessAreaSelect />
            </Box>
            <Box ml={6} data-cy="global-program-filter-container">
              <GlobalProgramSelect />
            </Box>
          </Box>
        </Box>
        <Box display="flex" justifyContent="flex-end">
          <Button startIcon={<TextsmsIcon style={{ color: '#e3e6e7' }} />}>
            <StyledLink target="_blank" href={servicenow}>
              Support
            </StyledLink>
          </Button>
          <UserProfileMenu meData={meData} />
        </Box>
      </StyledToolbar>
    </MuiAppBar>
  );
};
