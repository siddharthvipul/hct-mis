import React from 'react';
import styled from 'styled-components';
import { Paper, Typography } from '@material-ui/core';
import { TargetingCriteria } from './TargetingCriteria';
import { Results } from './Results';
import { TargetingHouseholds } from './TargetingHouseholds';

const PaperContainer = styled(Paper)`
  display: flex;
  padding: ${({ theme }) => theme.spacing(3)}px
    ${({ theme }) => theme.spacing(4)}px;
  margin: ${({ theme }) => theme.spacing(5)}px;
  flex-direction: column;
  border-bottom: 1px solid rgba(224, 224, 224, 1);
`;

const Label = styled.p`
  color: #b1b1b5;
`;

export function TargetPopulationCore({
  candidateList,
  targetPopulationList = null,
  id,
  selectedTab = 0,
  status,
  targetPopulation,
}) {
  if (!candidateList) return null;
  const { rules: candidateListRules } = candidateList;
  const totalNumOfHouseholds =
    selectedTab === 0
      ? targetPopulation.candidateListTotalHouseholds
      : targetPopulation.finalListTotalHouseholds;
  const totalNumOfIndividuals =
    selectedTab === 0
      ? targetPopulation.candidateListTotalIndividuals
      : targetPopulation.finalListTotalIndividuals;
  return (
    <>
      <TargetingCriteria
        selectedTab={selectedTab}
        candidateListRules={candidateListRules}
        targetPopulationRules={targetPopulationList?.rules}
      />
      <Results
        resultsData={
          selectedTab === 0
            ? targetPopulation.candidateStats
            : targetPopulation.finalStats
        }
        totalNumOfHouseholds={totalNumOfHouseholds}
        totalNumOfIndividuals={totalNumOfIndividuals}
      />
      {candidateListRules.length ? (
        <TargetingHouseholds
          id={id}
          status={status}
          selectedTab={selectedTab}
          candidateListTotalHouseholds={
            targetPopulation.candidateListTotalHouseholds
          }
          finalListTotalHouseholds={targetPopulation.finalListTotalHouseholds}
        />
      ) : (
        <PaperContainer>
          <Typography variant='h6'>
            Target Population Entries (Households)
          </Typography>
          <Label>Add targeting criteria to see results.</Label>
        </PaperContainer>
      )}
    </>
  );
}
