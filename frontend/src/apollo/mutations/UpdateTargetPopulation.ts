import { gql } from 'apollo-boost';

export const UpdateTP = gql`
  mutation UpdateTP($input: UpdateTargetPopulationInput!) {
    updateTargetPopulation(input: $input) {
      targetPopulation {
        id
        name
        status
        candidateListTotalHouseholds
        candidateListTotalIndividuals
        finalListTotalHouseholds
        finalListTotalIndividuals
        approvedAt
        finalizedAt
        finalizedBy {
          firstName
          lastName
        }
        program {
          id
          name
        }
        candidateListTargetingCriteria {
          targetPopulationCandidate {
            createdBy {
              firstName
              lastName
            }
            program {
              id
              name
            }
          }
          rules {
            id
            filters {
              fieldName
              isFlexField
              arguments
              comparisionMethod
              fieldAttribute {
                name
                labelEn
                type
                choices {
                  value
                  labelEn
                }
              }
            }
          }
        }
        finalListTargetingCriteria {
          targetPopulationFinal {
            createdBy {
              firstName
              lastName
            }
            program {
              id
              name
            }
          }
          rules {
            id
            filters {
              fieldName
              isFlexField
              arguments
              comparisionMethod
              fieldAttribute {
                name
                labelEn
                type
                choices {
                  value
                  labelEn
                }
              }
            }
          }
        }
        candidateStats{
          childMale
          childFemale
          adultMale
          adultFemale
        }
        finalStats{
          childMale
          childFemale
          adultMale
          adultFemale
        }
      }
    }
  }
`;
