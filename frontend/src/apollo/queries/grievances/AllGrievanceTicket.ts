import { gql } from 'apollo-boost';

export const AllGrievanceTicket = gql`
  query AllGrievanceTicket(
    $before: String
    $after: String
    $first: Int
    $last: Int
    $id: UUID
    $category: String
    $businessArea: String!
    $search: String
    $status: [String]
    $fsp: String
    $createdAtRange: String
    $admin: [ID]
    $orderBy: String
    $registrationDataImport: ID
    $assignedTo: ID
    $cashPlan: String
  ) {
    allGrievanceTicket(
      before: $before
      after: $after
      first: $first
      last: $last
      id: $id
      category: $category
      businessArea: $businessArea
      search: $search
      status: $status
      fsp: $fsp
      createdAtRange: $createdAtRange
      orderBy: $orderBy
      admin: $admin
      registrationDataImport: $registrationDataImport
      assignedTo: $assignedTo
      cashPlan: $cashPlan
    ) {
      totalCount
      pageInfo {
        startCursor
        endCursor
      }
      edges {
        cursor
        node {
          id
          status
          assignedTo {
            id
            firstName
            lastName
            email
          }
          createdBy {
            id
          }
          category
          createdAt
          userModified
          admin
          household {
            unicefId
            id
          }
          unicefId
        }
      }
    }
  }
`;