import { gql } from 'apollo-boost';

export const GrievanceTicket = gql`
  query GrievanceTicket($id: ID!) {
    grievanceTicket(id: $id) {
      id
      status
      category
      consent
      createdBy {
        id
        firstName
        lastName
        email
      }
      createdAt
      updatedAt
      description
      language
      admin
      area
      assignedTo {
        id
        firstName
        lastName
        email
      }
      individual {
        id
        unicefId
      }
      household {
        id
        unicefId
      }
      paymentRecord {
        id
      }
      issueType
      ticketNotes {
        edges {
          node {
            id
            createdAt
            updatedAt
            description
            createdBy {
              id
              firstName
              lastName
              email
            }
          }
        }
      }
    }
  }
`;
