export const PERMISSIONS = {
  // RDI
  RDI_VIEW_LIST: 'RDI_VIEW_LIST',
  RDI_VIEW_DETAILS: 'RDI_VIEW_DETAILS',
  RDI_IMPORT_DATA: 'RDI_IMPORT_DATA',
  RDI_RERUN_DEDUPE: 'RDI_RERUN_DEDUPE',
  RDI_MERGE_IMPORT: 'RDI_MERGE_IMPORT',

  // Population
  POPULATION_VIEW_HOUSEHOLDS_LIST: 'POPULATION_VIEW_HOUSEHOLDS_LIST',
  POPULATION_VIEW_HOUSEHOLDS_DETAILS: 'POPULATION_VIEW_HOUSEHOLDS_DETAILS',
  POPULATION_VIEW_INDIVIDUALS_LIST: 'POPULATION_VIEW_INDIVIDUALS_LIST',
  POPULATION_VIEW_INDIVIDUALS_DETAILS: 'POPULATION_VIEW_INDIVIDUALS_DETAILS',

  // User Management
  USER_MANAGEMENT_VIEW_LIST: 'USER_MANAGEMENT_VIEW_LIST',

  // Programme
  PRORGRAMME_VIEW_LIST_AND_DETAILS: 'PRORGRAMME_VIEW_LIST_AND_DETAILS',
  PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS:
    'PROGRAMME_VIEW_PAYMENT_RECORD_DETAILS',
  PROGRAMME_CREATE: 'PROGRAMME_CREATE',
  PROGRAMME_UPDATE: 'PROGRAMME_UPDATE',
  PROGRAMME_REMOVE: 'PROGRAMME_REMOVE',
  PROGRAMME_ACTIVATE: 'PROGRAMME_ACTIVATE',
  PROGRAMME_FINISH: 'PROGRAMME_FINISH',

  // Targeting
  TARGETING_VIEW_LIST: 'TARGETING_VIEW_LIST',
  TARGETING_VIEW_DETAILS: 'TARGETING_VIEW_DETAILS',
  TARGETING_CREATE: 'TARGETING_CREATE',
  TARGETING_UPDATE: 'TARGETING_UPDATE',
  TARGETING_DUPLICATE: 'TARGETING_DUPLICATE',
  TARGETING_REMOVE: 'TARGETING_REMOVE',
  TARGETING_LOCK: 'TARGETING_LOCK',
  TARGETING_UNLOCK: 'TARGETING_UNLOCK',
  TARGETING_SEND: 'TARGETING_SEND',

  // Payment Verification
  PAYMENT_VERIFICATION_VIEW_LIST: 'PAYMENT_VERIFICATION_VIEW_LIST',
  PAYMENT_VERIFICATION_VIEW_DETAILS: 'PAYMENT_VERIFICATION_VIEW_DETAILS',
  PAYMENT_VERIFICATION_CREATE: 'PAYMENT_VERIFICATION_CREATE',
  PAYMENT_VERIFICATION_UPDATE: 'PAYMENT_VERIFICATION_UPDATE',
  PAYMENT_VERIFICATION_ACTIVATE: 'PAYMENT_VERIFICATION_ACTIVATE',
  PAYMENT_VERIFICATION_DISCARD: 'PAYMENT_VERIFICATION_DISCARD',
  PAYMENT_VERIFICATION_FINISH: 'PAYMENT_VERIFICATION_FINISH',
  PAYMENT_VERIFICATION_EXPORT: 'PAYMENT_VERIFICATION_EXPORT',
  PAYMENT_VERIFICATION_IMPORT: 'PAYMENT_VERIFICATION_IMPORT',
  PAYMENT_VERIFICATION_VERIFY: 'PAYMENT_VERIFICATION_VERIFY',
  PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS:
    'PAYMENT_VERIFICATION_VIEW_PAYMENT_RECORD_DETAILS',

  // Grievances
  GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE:
    'GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE',
  GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_CREATOR:
    'GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_CREATOR',
  GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_OWNER:
    'GRIEVANCES_VIEW_LIST_EXCLUDING_SENSITIVE_AS_OWNER',
  GRIEVANCES_VIEW_LIST_SENSITIVE: 'GRIEVANCES_VIEW_LIST_SENSITIVE',
  GRIEVANCES_VIEW_LIST_SENSITIVE_AS_CREATOR:
    'GRIEVANCES_VIEW_LIST_SENSITIVE_AS_CREATOR',
  GRIEVANCES_VIEW_LIST_SENSITIVE_AS_OWNER:
    'GRIEVANCES_VIEW_LIST_SENSITIVE_AS_OWNER',
  GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE:
    'GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE',
  GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_CREATOR:
    'GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_CREATOR',
  GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_OWNER:
    'GRIEVANCES_VIEW_DETAILS_EXCLUDING_SENSITIVE_AS_OWNER',
  GRIEVANCES_VIEW_DETAILS_SENSITIVE: 'GRIEVANCES_VIEW_DETAILS_SENSITIVE',
  GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_CREATOR:
    'GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_CREATOR',
  GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_OWNER:
    'GRIEVANCES_VIEW_DETAILS_SENSITIVE_AS_OWNER',
  GRIEVANCES_VIEW_HOUSEHOLD_DETAILS: 'GRIEVANCES_VIEW_HOUSEHOLD_DETAILS',
  GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_CREATOR:
    'GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_CREATOR',
  GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_OWNER:
    'GRIEVANCES_VIEW_HOUSEHOLD_DETAILS_AS_OWNER',
  GRIEVANCES_VIEW_INDIVIDUALS_DETAILS: 'GRIEVANCES_VIEW_INDIVIDUALS_DETAILS',
  GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_CREATOR:
    'GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_CREATOR',
  GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_OWNER:
    'GRIEVANCES_VIEW_INDIVIDUALS_DETAILS_AS_OWNER',
  GRIEVANCES_CREATE: 'GRIEVANCES_CREATE',
  GRIEVANCES_UPDATE: 'GRIEVANCES_UPDATE',
  GRIEVANCES_UPDATE_AS_CREATOR: 'GRIEVANCES_UPDATE_AS_CREATOR',
  GRIEVANCES_UPDATE_AS_OWNER: 'GRIEVANCES_UPDATE_AS_OWNER',
  GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE:
    'GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE',
  GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_CREATOR:
    'GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_CREATOR',
  GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_OWNER:
    'GRIEVANCES_UPDATE_REQUESTED_DATA_CHANGE_AS_OWNER',
  GRIEVANCES_ADD_NOTE: 'GRIEVANCES_ADD_NOTE',
  GRIEVANCES_ADD_NOTE_AS_CREATOR: 'GRIEVANCES_ADD_NOTE_AS_CREATOR',
  GRIEVANCES_ADD_NOTE_AS_OWNER: 'GRIEVANCES_ADD_NOTE_AS_OWNER',
  GRIEVANCES_SET_IN_PROGRESS: 'GRIEVANCES_SET_IN_PROGRESS',
  GRIEVANCES_SET_IN_PROGRESS_AS_CREATOR:
    'GRIEVANCES_SET_IN_PROGRESS_AS_CREATOR',
  GRIEVANCES_SET_IN_PROGRESS_AS_OWNER: 'GRIEVANCES_SET_IN_PROGRESS_AS_OWNER',
  GRIEVANCES_SET_ON_HOLD: 'GRIEVANCES_SET_ON_HOLD',
  GRIEVANCES_SET_ON_HOLD_AS_CREATOR: 'GRIEVANCES_SET_ON_HOLD_AS_CREATOR',
  GRIEVANCES_SET_ON_HOLD_AS_OWNER: 'GRIEVANCES_SET_ON_HOLD_AS_OWNER',
  GRIEVANCES_SEND_FOR_APPROVAL: 'GRIEVANCES_SEND_FOR_APPROVAL',
  GRIEVANCES_SEND_FOR_APPROVAL_AS_CREATOR:
    'GRIEVANCES_SEND_FOR_APPROVAL_AS_CREATOR',
  GRIEVANCES_SEND_FOR_APPROVAL_AS_OWNER:
    'GRIEVANCES_SEND_FOR_APPROVAL_AS_OWNER',
  GRIEVANCES_SEND_BACK: 'GRIEVANCES_SEND_BACK',
  GRIEVANCES_SEND_BACK_AS_CREATOR: 'GRIEVANCES_SEND_BACK_AS_CREATOR',
  GRIEVANCES_SEND_BACK_AS_OWNER: 'GRIEVANCES_SEND_BACK_AS_OWNER',
  GRIEVANCES_APPROVE_DATA_CHANGE: 'GRIEVANCES_APPROVE_DATA_CHANGE',
  GRIEVANCES_APPROVE_DATA_CHANGE_AS_CREATOR:
    'GRIEVANCES_APPROVE_DATA_CHANGE_AS_CREATOR',
  GRIEVANCES_APPROVE_DATA_CHANGE_AS_OWNER:
    'GRIEVANCES_APPROVE_DATA_CHANGE_AS_OWNER',
  GRIEVANCES_APPROVE_FLAG_AND_DEDUPE: 'GRIEVANCES_APPROVE_FLAG_AND_DEDUPE',
  GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_CREATOR:
    'GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_CREATOR',
  GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_OWNER:
    'GRIEVANCES_APPROVE_FLAG_AND_DEDUPE_AS_OWNER',
  GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK:
    'GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK',
  GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_CREATOR:
    'GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_CREATOR',
  GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_OWNER:
    'GRIEVANCES_CLOSE_TICKET_EXCLUDING_FEEDBACK_AS_OWNER',
  GRIEVANCES_CLOSE_TICKET_FEEDBACK: 'GRIEVANCES_CLOSE_TICKET_FEEDBACK',
  GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_CREATOR:
    'GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_CREATOR',
  GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_OWNER:
    'GRIEVANCES_CLOSE_TICKET_FEEDBACK_AS_OWNER',

  // Reporting
  REPORTING_EXPORT: 'REPORTING_EXPORT',

  // Activity Log
  ACTIVITY_LOG_VIEW: 'ACTIVITY_LOG_VIEW',

  // Other
  ALL_VIEW_PII_DATA_ON_LISTS: 'ALL_VIEW_PII_DATA_ON_LISTS',

  // Dashboard
  DASHBOARD_VIEW_COUNTRY: 'DASHBOARD_VIEW_COUNTRY',
  DASHBOARD_EXPORT: 'DASHBOARD_EXPORT',
};

export function hasPermissions(
  permission: string | string[],
  allowedPermissions: string[],
): boolean {
  // checks to see if has one permission or at least one from the array

  if (Array.isArray(permission)) {
    return allowedPermissions.some((perm) => permission.includes(perm));
  }
  return allowedPermissions.includes(permission);
}

export function hasPermissionInModule(
  module: string,
  allowedPermissions: string[],
): boolean {
  return allowedPermissions.some((perm) => perm.includes(module));
}

export function hasCreatorOrOwnerPermissions(
  generalPermission: string,
  isCreator: boolean,
  creatorPermission: string,
  isOwner: boolean,
  ownerPermission: string,
  allowedPermissions: string[],
): boolean {
  // use where we have to check 3 different permissions, for ex. grievances
  return (
    allowedPermissions.includes(generalPermission) ||
    (isCreator && allowedPermissions.includes(creatorPermission)) ||
    (isOwner && allowedPermissions.includes(ownerPermission))
  );
}