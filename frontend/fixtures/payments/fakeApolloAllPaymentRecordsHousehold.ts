import { AllPaymentRecordsAndPaymentsDocument } from '../../src/__generated__/graphql';

export const fakeApolloAllPaymentRecordsHousehold = [
  {
    request: {
      query: AllPaymentRecordsAndPaymentsDocument,
      variables: {
        household:
          'SG91c2Vob2xkTm9kZTo3NjExNzM2Ny0yYWFiLTRmNTEtODUwOC1mMzBmODliYWUzYzE=',
        businessArea: 'afghanistan',
        first: 5,
        orderBy: null,
      },
    },
    result: {
      data: {
        allPaymentRecordsAndPayments: {
          pageInfo: {
            hasNextPage: false,
            hasPreviousPage: false,
            startCursor: 'YXJyYXljb25uZWN0aW9uOjA=',
            endCursor: 'YXJyYXljb25uZWN0aW9uOjM=',
            __typename: 'PageInfoNode',
          },
          edges: [
            {
              cursor: 'YXJyYXljb25uZWN0aW9uOjA=',
              node: {
                objType: 'PaymentRecord',
                id:
                  'UGF5bWVudFJlY29yZE5vZGU6ZWE4ZmU2OTktZGFhOS00NTE2LWE5NTktMzNkMzA3Y2M3ZWZm',
                fullName: 'Lisa Lewis',
                status: 'Pending',
                caId: '123-21-PR-00010',
                currency: 'IRR',
                entitlementQuantity: 4468.49,
                deliveredQuantity: 1308,
                deliveredQuantityUsd: 1966,
                deliveryDate: '2021-12-04 22:43:09+00:00',
                __typename: 'PaymentRecordAndPaymentNode',
              },
              __typename: 'PaymentRecordsAndPaymentsEdges',
            },
            {
              cursor: 'YXJyYXljb25uZWN0aW9uOjE=',
              node: {
                objType: 'PaymentRecord',
                id:
                  'UGF5bWVudFJlY29yZE5vZGU6MzE3ODUxYmYtNDU0YS00NDg4LWIyMzUtMjkzMDg5MTkyYzJj',
                fullName: 'Mark Mills',
                status: 'Distribution Successful',
                caId: '123-21-PR-00006',
                currency: 'LBP',
                entitlementQuantity: 1786.52,
                deliveredQuantity: 372,
                deliveredQuantityUsd: 298,
                deliveryDate: '2021-06-16 01:11:34+00:00',
                __typename: 'PaymentRecordAndPaymentNode',
              },
              __typename: 'PaymentRecordsAndPaymentsEdges',
            },
            {
              cursor: 'YXJyYXljb25uZWN0aW9uOjI=',
              node: {
                objType: 'PaymentRecord',
                id:
                  'UGF5bWVudFJlY29yZE5vZGU6MGVlODMzNzQtZDU1Yi00MzgwLTg1ZGQtNzM3MzE5ZmFjMWM0',
                fullName: 'Alisha Delacruz',
                status: 'Transaction Successful',
                caId: '123-21-PR-00003',
                currency: 'GBP',
                entitlementQuantity: 886.54,
                deliveredQuantity: 273,
                deliveredQuantityUsd: 583,
                deliveryDate: '2022-03-19 12:29:44+00:00',
                __typename: 'PaymentRecordAndPaymentNode',
              },
              __typename: 'PaymentRecordsAndPaymentsEdges',
            },
          ],
          totalCount: 4,
          __typename: 'PaginatedPaymentRecordsAndPaymentsNode',
        },
      },
    },
  },
];
