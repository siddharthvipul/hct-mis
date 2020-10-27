import { gql } from 'apollo-boost';

export const TARGET_POPULATION_QUERY = gql`
  query targetPopulation($id: ID!) {
    targetPopulation(id: $id) {
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
        startDate
        endDate
        status          
        caId
        description
        budget
        frequencyOfPayments
        populationGoal
        sector
        totalNumberOfHouseholds
        individualDataNeeded
      }
      createdBy {
        firstName
        lastName
      }
      candidateListTargetingCriteria {
        targetPopulationCandidate {
          createdBy {
            firstName
            lastName
          }
        }
        rules {
          id
          individualsFiltersBlocks{
            individualBlockFilters{
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
      candidateStats {
        childMale
        childFemale
        adultMale
        adultFemale
      }
      finalStats {
        childMale
        childFemale
        adultMale
        adultFemale
      }
    }
  }
`;
