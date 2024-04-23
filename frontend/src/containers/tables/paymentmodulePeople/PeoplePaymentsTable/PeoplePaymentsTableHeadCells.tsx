import { AllPaymentsForTableQuery } from '@generated/graphql';
import { HeadCell } from '@components/core/Table/EnhancedTableHead';

export const headCells: HeadCell<
  AllPaymentsForTableQuery['allPayments']['edges'][number]['node']
>[] = [
  {
    disablePadding: false,
    label: '',
    id: 'flag',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Payment Id',
    id: 'unicef_id',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Individual Id',
    id: 'individual__unicef_id',
    numeric: false,
    disableSort: true,
  },
  {
    disablePadding: false,
    label: 'Individual Name',
    id: 'individual__full_name',
    numeric: false,
    disableSort: true,
  },
  {
    disablePadding: false,
    label: 'Household Size',
    id: 'household__size',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Administrative Level 2',
    id: 'household__admin2__name',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'FSP',
    id: 'financial_service_provider__name',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Entitlement',
    id: 'entitlement_quantity_usd',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Delivered Quantity',
    id: 'delivered_quantity',
    numeric: false,
  },
  {
    disablePadding: false,
    label: 'Reconciliation',
    id: 'mark',
    numeric: false,
  },
];
