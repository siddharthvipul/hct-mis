import { ImportedHouseholdNode } from '../../src/__generated__/graphql';

export const fakeImportedHouseholdNode = {
  id:
    'SW1wb3J0ZWRIb3VzZWhvbGROb2RlOmEzY2I2NWFjLWRlMTMtNDQzYy04YThkLTJjZDJmYzM3ODkwYw==',
  headOfHousehold: {
    id:
      'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTozZTE0OGVkYy0wMTY3LTQ0ZTYtOTliYi02ZDA3MmM4ZjA2NWI=',
    fullName: 'Agata Kowalska',
    __typename: 'ImportedIndividualNode',
  },
  size: 4,
  admin1: 'AF06',
  admin1Title: 'Nangarhar',
  admin2: 'AF0617',
  admin2Title: 'Achin',
  flexFields: { months_displaced_h_f: 12 },
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
      'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOjljNzU3MTM4LTZmMDEtNGQzMS05YTM5LTdkZjFjMDA5NzE5ZA==',
    hctId: '30bb58c2-11ad-4208-8d5e-d435f0796e76',
    name: 'roamaniaks',
    __typename: 'RegistrationDataImportDatahubNode',
  },
  individuals: {
    edges: [
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTo0YmY3NmE4ZC05MmFjLTQwZjAtOTE2YS04ZDcwMDIwNzFiYmI=',
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
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOjljNzU3MTM4LTZmMDEtNGQzMS05YTM5LTdkZjFjMDA5NzE5ZA==',
            hctId: '30bb58c2-11ad-4208-8d5e-d435f0796e76',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTpjMjZiNmQ2MS1mMTdjLTQ0NmYtYjQ1MC0wMWI0NmMyYmE4Yjk=',
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
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOjljNzU3MTM4LTZmMDEtNGQzMS05YTM5LTdkZjFjMDA5NzE5ZA==',
            hctId: '30bb58c2-11ad-4208-8d5e-d435f0796e76',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
      {
        node: {
          id:
            'SW1wb3J0ZWRJbmRpdmlkdWFsTm9kZTozZTE0OGVkYy0wMTY3LTQ0ZTYtOTliYi02ZDA3MmM4ZjA2NWI=',
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
              'UmVnaXN0cmF0aW9uRGF0YUltcG9ydERhdGFodWJOb2RlOjljNzU3MTM4LTZmMDEtNGQzMS05YTM5LTdkZjFjMDA5NzE5ZA==',
            hctId: '30bb58c2-11ad-4208-8d5e-d435f0796e76',
            __typename: 'RegistrationDataImportDatahubNode',
          },
          __typename: 'ImportedIndividualNode',
        },
        __typename: 'ImportedIndividualNodeEdge',
      },
    ],
    __typename: 'ImportedIndividualNodeConnection',
  },
} as ImportedHouseholdNode;
