import DashboardIcon from '@material-ui/icons/DashboardRounded';
import AutorenewIcon from '@material-ui/icons/AutorenewRounded';
import PeopleIcon from '@material-ui/icons/PeopleRounded';
import ListAltRounded from '@material-ui/icons/ListAltRounded';
import FlashOnRounded from '@material-ui/icons/FlashOnRounded';
import FaceIcon from '@material-ui/icons/Face';
import AttachMoney from '@material-ui/icons/AttachMoney';
import Feedback from '@material-ui/icons/Feedback';
import TrendingUpRounded from '@material-ui/icons/TrendingUpRounded';
import SupervisedUserCircle from '@material-ui/icons/SupervisedUserCircle';
import SettingsRounded from '@material-ui/icons/SettingsRounded';
import PeopleAltRoundedIcon from '@material-ui/icons/PeopleAltRounded';
import React from 'react';

export const menuItems = [
  {
    name: 'Country Dashboard',
    href: '/#',
    selectedRegexp: /^\/test.*$/,
    icon: <DashboardIcon />,
  },
  {
    name: 'Registration Data Import',
    href: '/registration-data-import',
    selectedRegexp: /^\/registration-data-import.*$/,
    icon: <AutorenewIcon />,
    permissionModule: 'RDI',
  },
  {
    name: 'Population',
    href: '/population/household',
    selectedRegexp: /^\/population.*$/,
    icon: <PeopleIcon />,
    collapsable: true,
    secondaryActions: [
      {
        name: 'Households',
        href: '/population/household',
        selectedRegexp: /^\/population\/household.*$/,
        icon: <PeopleAltRoundedIcon />,
      },
      {
        name: 'Individuals',
        href: '/population/individuals',
        selectedRegexp: /^\/population\/individuals.*$/,
        icon: <FaceIcon />,
      },
    ],
  },
  {
    name: 'Programme Management',
    href: '/programs',
    selectedRegexp: /^\/programs.*$/,
    icon: <FlashOnRounded />,
  },
  {
    name: 'Targeting',
    href: '/target-population',
    selectedRegexp: /^\/target-population.*$/,
    icon: <ListAltRounded />,
  },
  {
    name: 'Payment Verification',
    href: '/payment-verification',
    selectedRegexp: /^\/payment-verification*$/,
    icon: <AttachMoney />,
  },
  {
    name: 'Grievance and Feedback',
    href: '/grievance-and-feedback',
    selectedRegexp: /^\/test.*$/,
    icon: <Feedback />,
  },
  {
    name: 'Reporting',
    href: '/#',
    selectedRegexp: /^\/test.*$/,
    icon: <TrendingUpRounded />,
  },
  {
    name: 'User Management',
    href: '/users-list',
    selectedRegexp: /^\/test.*$/,
    icon: <SupervisedUserCircle />,
  },
  {
    name: 'Settings',
    href: '/#',
    selectedRegexp: /^\/test.*$/,
    icon: <SettingsRounded />,
  },
];
