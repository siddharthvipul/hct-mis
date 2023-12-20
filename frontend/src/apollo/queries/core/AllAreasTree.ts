import { gql } from 'apollo-boost';

export const ALL_AREAS_TREE_QUERY = gql`
  query AllAreasTree($businessArea: String!) {
    allAreasTree(businessArea: $businessArea) {
      id
      name
      pCode
      areas {
        id
        name
        pCode
        areas {
          id
          name
          pCode
          areas {
            id
            name
            pCode
          }
        }
      }
    }
  }
`;