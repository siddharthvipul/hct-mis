import { gql } from 'apollo-boost';

export const AllCashPlans = gql`
    query AllCashPlans($program:ID!,$after:String,$count:Int){

        allCashPlans(program: $program, after: $after,first: $count) {
            pageInfo {
                hasNextPage
                hasPreviousPage
                startCursor
                endCursor
            }
            totalCount
            edges{
                cursor
                node{
                    id
                    cashAssistId
                    numberOfHouseholds
                    disbursementDate
                    currency
                    status
                    totalEntitledQuantity
                    totalDeliveredQuantity
                    totalUndeliveredQuantity
                }
            }
        }
    } `;
