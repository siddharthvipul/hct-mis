import { ImportedHouseholdDetailedFragment } from '../../src/__generated__/graphql';

export const fakeImportedHouseholdDetailedFragment = {
  id:
    'SW1wb3J0ZWRIb3VzZWhvbGROb2RlOjdhZDk2Zjc0LTJhODAtNDQxNS1hYWZlLTBjNjRjMWQ2ZWQ1NQ==',
  headOfHousehold: {
    id:
      'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTpmM2U0ODBiZC05MDYyLTRkMjktODljYy1kMWM3MGRhZDRmMjk=',
    fullName: 'Agata Kowalska',
    __typename: 'ImportedIndividualNode',
  },
  size: 4,
  admin1: 'AF06',
  admin1Title: 'Nangarhar',
  admin2: 'AF0617',
  admin2Title: 'Achin',
  flexFields: { months_displaced_h_f: 12, difficulty_breathing_h_f: '1' },
  deviceid: '',
  start: null,
  firstRegistrationDate: '2020-08-22T00:00:00',
  lastRegistrationDate: '2020-08-22T00:00:00',
  hasDuplicates: false,
  fchildHoh: false,
  childHoh: false,
  __typename: 'ImportedHouseholdNode',
  residenceStatus: 'REFUGEE',
  country: 'Isle of Man',
  countryOrigin: 'San Marino',
  registrationDataImport: {
    id:
      'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOmE1YzAyNWU0LTAwMTAtNDA0Yy04YTIyLTUxNWUwNjA5ZDQ2OQ==',
    hctId: '8cc865bb-c993-489d-a6b5-5ceb21c6a0c3',
    name: 'romaniaks',
    __typename: 'RegistrationDataImportDatahubNode',
  },
  individuals: {
    edges: [
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTphODQ0OTY3OS0wNzcxLTQwODAtYjlhMy05ZTUxNDVjNGRiZmE=',
          age: 80,
          fullName: 'Alicja Kowalska',
          birthDate: '1941-08-26',
          sex: 'FEMALE',
          role: 'ALTERNATE',
          relationship: 'NON_BENEFICIARY',
          deduplicationBatchStatus: 'UNIQUE_IN_BATCH',
          deduplicationGoldenRecordStatus: 'UNIQUE',
          deduplicationGoldenRecordResults: [],
          deduplicationBatchResults: [],
          registrationDataImport: {
            id:
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOmE1YzAyNWU0LTAwMTAtNDA0Yy04YTIyLTUxNWUwNjA5ZDQ2OQ==',
            hctId: '8cc865bb-c993-489d-a6b5-5ceb21c6a0c3',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZToxMGQ1NzA3My1mZWMwLTQwZmMtODk3OC02MzkzNTI4YjE3ODU=',
          age: 22,
          fullName: 'Angela Kowalska',
          birthDate: '2000-01-10',
          sex: 'FEMALE',
          role: 'NO_ROLE',
          relationship: 'BROTHER_SISTER',
          deduplicationBatchStatus: 'UNIQUE_IN_BATCH',
          deduplicationGoldenRecordStatus: 'UNIQUE',
          deduplicationGoldenRecordResults: [],
          deduplicationBatchResults: [],
          registrationDataImport: {
            id:
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOmE1YzAyNWU0LTAwMTAtNDA0Yy04YTIyLTUxNWUwNjA5ZDQ2OQ==',
            hctId: '8cc865bb-c993-489d-a6b5-5ceb21c6a0c3',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTpmM2U0ODBiZC05MDYyLTRkMjktODljYy1kMWM3MGRhZDRmMjk=',
          age: 58,
          fullName: 'Agata Kowalska',
          birthDate: '1964-01-10',
          sex: 'FEMALE',
          role: 'PRIMARY',
          relationship: 'HEAD',
          deduplicationBatchStatus: 'UNIQUE_IN_BATCH',
          deduplicationGoldenRecordStatus: 'UNIQUE',
          deduplicationGoldenRecordResults: [],
          deduplicationBatchResults: [],
          registrationDataImport: {
            id:
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOmE1YzAyNWU0LTAwMTAtNDA0Yy04YTIyLTUxNWUwNjA5ZDQ2OQ==',
            hctId: '8cc865bb-c993-489d-a6b5-5ceb21c6a0c3',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
    ],
    __typename: 'ImportedIndividualNodeConnection',
  },
} as ImportedHouseholdDetailedFragment;
