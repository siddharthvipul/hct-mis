import { GraphQLError } from 'graphql';
import { useHistory, useLocation, LocationState } from 'react-router-dom';
import localForage from 'localforage';
import camelCase from 'lodash/camelCase';
import { ValidationGraphQLError } from '../apollo/ValidationGraphQLError';
import { theme as themeObj } from '../theme';
import {
  AllProgramsQuery,
  ChoiceObject,
  PaymentPlanBackgroundActionStatus,
  PaymentPlanStatus,
  PaymentRecordStatus,
  PaymentStatus,
  ProgramStatus,
  TargetPopulationBuildStatus,
  TargetPopulationStatus,
} from '../__generated__/graphql';
import {
  GRIEVANCE_CATEGORIES,
  PAYMENT_PLAN_BACKGROUND_ACTION_STATES,
  PAYMENT_PLAN_STATES,
  PROGRAM_STATES,
  TARGETING_STATES,
} from './constants';

const Gender = new Map([
  ['MALE', 'Male'],
  ['FEMALE', 'Female'],
]);

const IdentificationType = new Map([
  ['NA', 'N/A'],
  ['BIRTH_CERTIFICATE', 'Birth Certificate'],
  ['DRIVING_LICENSE', 'Driving License'],
  ['UNHCR_ID_CARD', 'UNHCR ID Card'],
  ['NATIONAL_ID', 'National ID'],
  ['NATIONAL_PASSPORT', 'National Passport'],
]);

export const getIdentificationType = (idType: string): string => {
  if (IdentificationType.has(idType)) {
    return IdentificationType.get(idType);
  }
  return idType;
};
export const sexToCapitalize = (sex: string): string => {
  if (Gender.has(sex)) {
    return Gender.get(sex);
  }
  return sex;
};

export function opacityToHex(opacity: number): string {
  return Math.floor(opacity * 0xff).toString(16);
}

export function programStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case ProgramStatus.Draft:
      return theme.hctPalette.gray;
    case ProgramStatus.Active:
      return theme.hctPalette.green;
    case ProgramStatus.Finished:
      return theme.hctPalette.gray;
    default:
      return theme.hctPalette.orange;
  }
}
export function maritalStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'SINGLE':
      return theme.hctPalette.green;
    case 'MARRIED':
      return theme.hctPalette.orange;
    case 'WIDOW':
      return theme.hctPalette.gray;
    case 'DIVORCED':
      return theme.hctPalette.gray;
    case 'SEPARATED':
      return theme.hctPalette.gray;
    default:
      return theme.hctPalette.gray;
  }
}
export function populationStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'ACTIVE':
      return theme.hctPalette.green;
    default:
      return theme.hctPalette.gray;
  }
}

export function cashPlanStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'DISTRIBUTION_COMPLETED':
      return theme.hctPalette.green;
    case 'TRANSACTION_COMPLETED':
      return theme.hctPalette.green;
    default:
      return theme.palette.error.main;
  }
}
export function paymentRecordStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case PaymentRecordStatus.Pending:
      return theme.hctPalette.orange;
    case PaymentRecordStatus.DistributionSuccessful:
    case PaymentRecordStatus.TransactionSuccessful:
      return theme.hctPalette.green;
    case PaymentRecordStatus.PartiallyDistributed:
      return theme.hctPalette.lightBlue;
    default:
      return theme.palette.error.main;
  }
}

export function paymentStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case PaymentStatus.Pending:
      return theme.hctPalette.orange;
    case PaymentStatus.DistributionSuccessful:
    case PaymentStatus.TransactionSuccessful:
      return theme.hctPalette.green;
    case PaymentStatus.PartiallyDistributed:
      return theme.hctPalette.lightBlue;
    default:
      return theme.palette.error.main;
  }
}
export function paymentVerificationStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'ACTIVE':
      return theme.hctPalette.green;
    case 'PENDING':
      return theme.hctPalette.orange;
    case 'FINISHED':
      return theme.hctPalette.gray;
    default:
      return theme.palette.error.main;
  }
}

export function verificationRecordsStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'PENDING':
      return theme.hctPalette.gray;
    case 'RECEIVED':
      return theme.hctPalette.green;
    case 'NOT_RECEIVED':
      return theme.palette.error.main;
    case 'RECEIVED_WITH_ISSUES':
      return theme.hctPalette.orange;
    default:
      return theme.palette.error.main;
  }
}
export function registrationDataImportStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'APPROVED':
      return theme.hctPalette.green;
    case 'MERGED':
      return theme.hctPalette.gray;
    case 'IN_PROGRESS':
      return theme.hctPalette.orange;
    default:
      return theme.hctPalette.orange;
  }
}

export function targetPopulationStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  const colorsMap = {
    [TargetPopulationStatus.Open]: theme.hctPalette.gray,
    [TargetPopulationStatus.Locked]: theme.hctPalette.red,
    [TargetPopulationStatus.Processing]: theme.hctPalette.blue,
    [TargetPopulationStatus.ReadyForCashAssist]: theme.hctPalette.green,
    [TargetPopulationStatus.ReadyForPaymentModule]: theme.hctPalette.green,
    [TargetPopulationStatus.Assigned]: theme.hctPalette.green,
    [TargetPopulationStatus.SteficonWait]: theme.hctPalette.orange,
    [TargetPopulationStatus.SteficonRun]: theme.hctPalette.blue,
    [TargetPopulationStatus.SteficonCompleted]: theme.hctPalette.green,
    [TargetPopulationStatus.SteficonError]: theme.palette.error.main,
  };
  if (status in colorsMap) {
    return colorsMap[status];
  }
  return theme.palette.error.main;
}

export function targetPopulationBuildStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  const colorsMap = {
    [TargetPopulationBuildStatus.Ok]: theme.hctPalette.green,
    [TargetPopulationBuildStatus.Failed]: theme.hctPalette.red,
    [TargetPopulationBuildStatus.Building]: theme.hctPalette.orange,
    [TargetPopulationBuildStatus.Pending]: theme.hctPalette.gray,
  };
  if (status in colorsMap) {
    return colorsMap[status];
  }
  return theme.palette.error.main;
}

export function paymentPlanStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  const colorsMap = {
    [PaymentPlanStatus.Preparing]: theme.hctPalette.gray,
    [PaymentPlanStatus.Open]: theme.hctPalette.gray,
    [PaymentPlanStatus.Locked]: theme.hctPalette.orange,
    [PaymentPlanStatus.LockedFsp]: theme.hctPalette.orange,
    [PaymentPlanStatus.InApproval]: theme.hctPalette.darkerBlue,
    [PaymentPlanStatus.InAuthorization]: theme.hctPalette.darkerBlue,
    [PaymentPlanStatus.InReview]: theme.hctPalette.blue,
    [PaymentPlanStatus.Accepted]: theme.hctPalette.green,
    [PaymentPlanStatus.Finished]: theme.hctPalette.green,
  };
  if (status in colorsMap) {
    return colorsMap[status];
  }
  return theme.palette.error.main;
}

export function paymentPlanBackgroundActionStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  const colorsMap = {
    [PaymentPlanBackgroundActionStatus.RuleEngineRun]: theme.hctPalette.gray,
    [PaymentPlanBackgroundActionStatus.RuleEngineError]:
      theme.palette.error.main,
    [PaymentPlanBackgroundActionStatus.XlsxExporting]: theme.hctPalette.gray,
    [PaymentPlanBackgroundActionStatus.XlsxExportError]:
      theme.palette.error.main,
    [PaymentPlanBackgroundActionStatus.XlsxImportingEntitlements]:
      theme.hctPalette.gray,
    [PaymentPlanBackgroundActionStatus.XlsxImportingReconciliation]:
      theme.hctPalette.gray,
    [PaymentPlanBackgroundActionStatus.XlsxImportError]:
      theme.palette.error.main,
  };
  if (status in colorsMap) {
    return colorsMap[status];
  }
  return theme.palette.error.main;
}

export function userStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'INVITED':
      return theme.hctPalette.gray;
    case 'ACTIVE':
      return theme.hctPalette.green;
    case 'INACTIVE':
      return theme.palette.error.main;
    default:
      return theme.palette.error.main;
  }
}

export function householdStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'ACTIVE':
      return theme.hctPalette.green;
    case 'INACTIVE':
      return theme.palette.error.main;
    default:
      return theme.palette.error.main;
  }
}

export function grievanceTicketStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'New':
      return theme.hctPalette.orange;
    case 'Assigned':
      return theme.hctPalette.darkerBlue;
    case 'In Progress':
      return theme.hctPalette.green;
    case 'On Hold':
      return theme.palette.error.main;
    case 'For Approval':
      return theme.hctPalette.darkBrown;
    case 'Closed':
      return theme.hctPalette.gray;
    default:
      return theme.palette.error.main;
  }
}

export function reportStatusToColor(
  theme: typeof themeObj,
  status: string,
): string {
  switch (status) {
    case 'Generated':
      return theme.hctPalette.green;
    case 'Processing':
      return theme.hctPalette.gray;
    default:
      return theme.palette.error.main;
  }
}

export function selectFields(
  fullObject,
  keys: string[],
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
): { [key: string]: any } {
  return keys.reduce((acc, current) => {
    acc[current] = fullObject[current];
    return acc;
  }, {});
}

export function camelToUnderscore(key): string {
  return key.replace(/([A-Z])/g, '_$1').toLowerCase();
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function camelizeObjectKeys(obj): { [key: string]: any } {
  if (!obj) {
    return obj;
  }
  return Object.keys(obj).reduce((acc, current) => {
    if (typeof obj[current] === 'object') {
      acc[camelToUnderscore(current)] = camelizeObjectKeys(obj[current]);
    } else {
      acc[camelCase(current)] = obj[current];
    }
    return acc;
  }, {});
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function camelizeArrayObjects(arr): { [key: string]: any }[] {
  if (!arr) {
    return arr;
  }
  return arr.map(camelizeObjectKeys);
}

export function columnToOrderBy(
  column: string,
  orderDirection: string,
): string {
  if (column.startsWith('-')) {
    const clearColumn = column.replace('-', '');
    return camelToUnderscore(
      `${orderDirection === 'asc' ? '-' : ''}${clearColumn}`,
    );
  }
  return camelToUnderscore(`${orderDirection === 'desc' ? '-' : ''}${column}`);
}

export function choicesToDict(
  choices: ChoiceObject[],
): { [key: string]: string } {
  if (!choices) return {};
  return choices.reduce((previousValue, currentValue) => {
    const newDict = { ...previousValue };
    newDict[currentValue.value] = currentValue.name;
    return newDict;
  }, {});
}

export function programStatusToPriority(status: ProgramStatus): number {
  switch (status) {
    case ProgramStatus.Draft:
      return 1;
    case ProgramStatus.Active:
      return 2;
    default:
      return 3;
  }
}
export function decodeIdString(idString): string | null {
  if (!idString) {
    return null;
  }
  const decoded = atob(idString);
  return decoded.split(':')[1];
}

export function programCompare(
  a: AllProgramsQuery['allPrograms']['edges'][number],
  b: AllProgramsQuery['allPrograms']['edges'][number],
): number {
  const statusA = programStatusToPriority(a.node.status);
  const statusB = programStatusToPriority(b.node.status);
  return statusA > statusB ? 1 : -1;
}

export function formatCurrency(
  amount: number,
  onlyNumberValue = false,
): string {
  const amountCleared = amount || 0;
  return `${amountCleared.toLocaleString('en-US', {
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}${onlyNumberValue ? '' : ' USD'}`;
}

export function formatCurrencyWithSymbol(
  amount: number,
  currency = 'USD',
): string {
  const amountCleared = amount || 0;
  // if currency is unknown, simply format using most common formatting option, and don't show currency symbol
  if (!currency) return formatCurrency(amountCleared, true);
  // undefined forces to use local browser settings
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency,
    // enable this if decided that we always want code and not a symbol
    currencyDisplay: 'code',
  }).format(amountCleared);
}

export function countPercentage(
  partialValue: number,
  totalValue: number,
): number {
  if (!totalValue || !partialValue) return 0;
  return +((partialValue / totalValue) * 100).toFixed(2);
}

export function getPercentage(
  partialValue: number,
  totalValue: number,
): string {
  return `${countPercentage(partialValue, totalValue)}%`;
}

export function formatNumber(value: number): string {
  if (!value && value !== 0) return '';
  return value.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export function formatThousands(value: string): string {
  if (!value) return value;
  if (parseInt(value, 10) >= 10000) {
    return `${value.toString().slice(0, -3)}k`;
  }
  return value;
}

export function targetPopulationStatusMapping(status): string {
  return TARGETING_STATES[status];
}

export function programStatusMapping(status): string {
  return PROGRAM_STATES[status];
}

export function paymentPlanStatusMapping(status): string {
  return PAYMENT_PLAN_STATES[status];
}

export function paymentPlanBackgroundActionStatusMapping(status): string {
  return PAYMENT_PLAN_BACKGROUND_ACTION_STATES[status];
}

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

export function descendingComparator(a, b, orderBy): number {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

export function getComparator(
  order,
  orderBy,
): (a: number, b: number) => number {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

export function renderUserName(user): string {
  if (!user) {
    return '-';
  }
  return user?.firstName
    ? `${user?.firstName} ${user?.lastName}`
    : `${user?.email}`;
}

export const getPhoneNoLabel = (
  phoneNo: string,
  phoneNoValid?: boolean,
): string => {
  if (!phoneNo) return '-';
  if (phoneNoValid === false) {
    return 'Invalid Phone Number';
  }
  return phoneNo;
};

const grievanceTypeIssueTypeDict: { [id: string]: boolean | string } = {
  [GRIEVANCE_CATEGORIES.NEGATIVE_FEEDBACK]: false,
  [GRIEVANCE_CATEGORIES.POSITIVE_FEEDBACK]: false,
  [GRIEVANCE_CATEGORIES.REFERRAL]: false,
  [GRIEVANCE_CATEGORIES.GRIEVANCE_COMPLAINT]: false,
  [GRIEVANCE_CATEGORIES.SENSITIVE_GRIEVANCE]: true,
  [GRIEVANCE_CATEGORIES.DATA_CHANGE]: true,
};

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export function thingForSpecificGrievanceType(
  ticket: { category: number | string; issueType?: number | string },
  thingDict,
  defaultThing = null,
  categoryWithIssueTypeDict = grievanceTypeIssueTypeDict,
) {
  const category = ticket.category?.toString();
  const issueType = ticket.issueType?.toString();
  if (!(category in thingDict)) {
    return defaultThing;
  }
  const categoryThing = thingDict[category];
  if (
    categoryWithIssueTypeDict[category] === 'IGNORE' ||
    (!categoryWithIssueTypeDict[category] &&
      (issueType === null || issueType === undefined))
  ) {
    return categoryThing;
  }
  if (!(issueType in categoryThing)) {
    return defaultThing;
  }
  return categoryThing[issueType];
}

export const isInvalid = (fieldname: string, errors, touched): boolean =>
  errors[fieldname] && touched[fieldname];

export const anon = (inputStr: string, shouldAnonymize: boolean): string => {
  if (!inputStr) return null;
  return shouldAnonymize
    ? inputStr
        .split(' ')
        .map((el) => el.substring(0, 2) + '*'.repeat(3))
        .join(' ')
    : inputStr;
};

export const isPermissionDeniedError = (error): boolean =>
  error?.message.includes('Permission Denied');

// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
export const getFullNodeFromEdgesById = (edges, id) => {
  if (!edges) return null;
  return edges.find((edge) => edge.node.id === id)?.node || null;
};

export const getFlexFieldTextValue = (key, value, fieldAttribute): string => {
  let textValue = value;
  if (!fieldAttribute) return textValue;
  if (fieldAttribute.type === 'SELECT_ONE') {
    textValue =
      fieldAttribute.choices.find((item) => item.value === value)?.labelEn ||
      value;
  }
  if (fieldAttribute.type === 'SELECT_MANY') {
    const values = fieldAttribute.choices.filter((item) =>
      value.includes(item.value),
    );
    textValue = values.map((item) => item.labelEn).join(', ');
  }
  return textValue;
};

export const handleValidationErrors = (
  fieldName,
  e,
  setFieldError,
  showMessage,
): { nonValidationErrors: GraphQLError[] } => {
  const validationErrors = e.graphQLErrors.filter(
    (error) => error instanceof ValidationGraphQLError,
  );
  const nonValidationErrors = e.graphQLErrors.filter(
    (error) => !(error instanceof ValidationGraphQLError),
  );
  for (const validationError of validationErrors) {
    Object.entries(validationError.validationErrors[fieldName]).map(
      // eslint-disable-next-line array-callback-return
      (entry) => {
        if (entry[0] === '__all__') {
          showMessage((entry[1] as string[]).join('\n'));
        }
        setFieldError(entry[0], (entry[1] as string[]).join('\n'));
      },
    );
  }
  return { nonValidationErrors };
};

export function renderSomethingOrDash(something): number | string | boolean {
  if (something === null || something === undefined) {
    return '-';
  }
  return something;
}

export function renderBoolean(booleanValue: boolean): string {
  if (booleanValue === null || booleanValue === undefined) {
    return '-';
  }
  switch (booleanValue) {
    case true:
      return 'Yes';
    default:
      return 'No';
  }
}

export const formatAge = (age): string | number => {
  if (age > 0) {
    return age;
  }
  return '<1';
};

export const renderIndividualName = (individual): string => {
  return individual?.fullName;
};

export async function clearCache(apolloClient = null): Promise<void> {
  if (apolloClient) apolloClient.resetStore();
  localStorage.clear();
  await localForage.clear();
}

type Location = ReturnType<typeof useLocation>;
type FilterValue = string | string[] | boolean | null | undefined;
type Filter = { [key: string]: FilterValue };

export const getFilterFromQueryParams = (
  location: Location,
  initialFilter: Filter = {},
): Filter => {
  const filter: Filter = { ...initialFilter };
  const searchParams = new URLSearchParams(location.search);
  for (const [key, value] of searchParams.entries()) {
    if (key in filter) {
      const existingValue = filter[key];
      if (Array.isArray(existingValue)) {
        const values = value.split(',');
        filter[key] = [...existingValue, ...values];
      } else {
        filter[key] =
          value !== 'true' && value !== 'false' ? value : value === 'true';
      }
    }
  }
  return filter;
};

export const setQueryParam = (
  key: string,
  value: string,
  history: useHistory<LocationState>,
  location: Location,
): void => {
  const params = new URLSearchParams(location.search);

  // Remove all existing values for the given key
  params.delete(key);

  // Add the new value for the given key
  params.append(key, value);

  history.push({ search: params.toString() });
};

export const setFilterToQueryParams = (
  filter: { [key: string]: FilterValue },
  history: useHistory<LocationState>,
  location: Location,
): void => {
  const params = new URLSearchParams(location.search);
  Object.entries(filter).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      if (Array.isArray(value)) {
        // remove all existing params for this key
        params.delete(key);

        // add each value as a separate param
        value.forEach((val) => {
          if (val !== null && val !== undefined) {
            params.append(key, val);
          }
        });
      } else {
        const paramValue =
          typeof value === 'boolean' ? value.toString() : value;
        params.set(key, paramValue);
      }
    } else {
      params.delete(key);
    }
  });
  const search = params.toString();
  history.push({ search });
};

export const createHandleFilterChange = (
  onFilterChange: (filter: { [key: string]: FilterValue }) => void,
  initialFilter: Filter,
  history: useHistory<LocationState>,
  location: Location,
): ((key: string, value: FilterValue) => void) => {
  let filterFromQueryParams = getFilterFromQueryParams(location, initialFilter);

  const handleFilterChange = (key: string, value: FilterValue): void => {
    const newFilter = {
      ...filterFromQueryParams,
      [key]: value,
    };

    filterFromQueryParams = newFilter;
    onFilterChange(newFilter);

    const params = new URLSearchParams(location.search);
    const isEmpty = (v: FilterValue): boolean =>
      v === '' ||
      v === null ||
      v === undefined ||
      (Array.isArray(v) && v.length === 0);

    if (isEmpty(value)) {
      params.delete(key);
    } else if (Array.isArray(value)) {
      const filteredValues = value.filter((v) => !isEmpty(v));
      if (filteredValues.length > 0) {
        params.set(key, filteredValues.join(','));
      } else {
        params.delete(key);
      }
    } else {
      params.set(key, value.toString());
    }

    const search = params.toString();
    history.push({ search });
  };

  return handleFilterChange;
};

export const tomorrow = new Date().setDate(new Date().getDate() + 1);
export const today = new Date();
today.setHours(0, 0, 0, 0);

export const removeBracketsAndQuotes = (str: string): string => {
  let modifiedStr = str;
  modifiedStr = modifiedStr.replace(/\[|\]|"|'/g, '');
  return modifiedStr;
};
