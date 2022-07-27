import { gql } from 'apollo-boost';

export const AllTargetPopulations = gql`
  query AllTargetPopulations(
    $after: String
    $before: String
    $first: Int
    $last: Int
    $orderBy: String
    $name: String
    $status: String
    $numberOfHouseholdsMin: Int
    $numberOfHouseholdsMax: Int
    $businessArea: String
    $program: [ID]
    $paymentPlanApplicable: Boolean
  ) {
    allTargetPopulation(
      after: $after
      before: $before
      first: $first
      last: $last
      orderBy: $orderBy
      name: $name
      status: $status
      numberOfHouseholdsMin: $numberOfHouseholdsMin
      numberOfHouseholdsMax: $numberOfHouseholdsMax
      businessArea: $businessArea
      program: $program
      paymentPlanApplicable: $paymentPlanApplicable
    ) {
      edges {
        node {
          ...targetPopulationMinimal
        }
        cursor
      }
      totalCount
      edgeCount
    }
  }
`;
