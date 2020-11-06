import { HeadCell } from '../../table/EnhancedTableHead';
import { GrievanceTicketNode } from '../../../__generated__/graphql';

export const headCells: HeadCell<GrievanceTicketNode>[] = [
  {
    disablePadding: false,
    label: '',
    id: 'checkbox',
    numeric: false,
    dataCy: 'ticket-id-checkbox',
  },
  {
    disablePadding: false,
    label: 'Ticket Id',
    id: 'id',
    numeric: false,
    dataCy: 'ticket-id',
  },
  {
    disablePadding: false,
    label: 'Status',
    id: 'status',
    numeric: false,
    dataCy: 'status',
  },
  {
    disablePadding: false,
    label: 'Category',
    id: 'category',
    numeric: false,
    dataCy: 'category',
  },
  {
    disablePadding: false,
    label: 'Household Id',
    id: 'householdId',
    numeric: false,
    dataCy: 'householdId',
  },
  {
    disablePadding: false,
    label: 'Assigned to',
    id: 'assignedTo',
    numeric: false,
    dataCy: 'assignedTo',
  },

  {
    disablePadding: false,
    label: 'Administrative Level 2',
    id: 'admin',
    numeric: false,
    dataCy: 'admin',
  },
];
