import { Typography } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import React from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { useArrayToDict } from '../../hooks/useArrayToDict';
import {
  IndividualNode,
  useAllIndividualsFlexFieldsAttributesQuery,
} from '../../__generated__/graphql';
import { LabelizedField } from '../LabelizedField';
import { LoadingComponent } from '../LoadingComponent';

const Overview = styled(Paper)`
  padding: ${({ theme }) => theme.spacing(8)}px
    ${({ theme }) => theme.spacing(11)}px;
  margin-top: ${({ theme }) => theme.spacing(6)}px;
  margin-bottom: ${({ theme }) => theme.spacing(6)}px;
`;

const Title = styled.div`
  width: 100%;
  padding-bottom: ${({ theme }) => theme.spacing(8)}px;
`;

const Image = styled.img`
  max-width: 150px;
`;

interface IndividualVulnerabilitesProps {
  individual: IndividualNode;
}

export function IndividualVulnerabilities({
  individual,
}: IndividualVulnerabilitesProps): React.ReactElement {
  const { t } = useTranslation();
  const { data, loading } = useAllIndividualsFlexFieldsAttributesQuery();
  const flexAttributesDict = useArrayToDict(
    data?.allIndividualsFlexFieldsAttributes,
    'name',
    '*',
  );

  if (loading) {
    return <LoadingComponent />;
  }

  if (!data || !flexAttributesDict) {
    return null;
  }

  const fields = Object.entries(individual.flexFields || {}).map(
    ([key, value]: [string, string | string[]]) => {
      if (flexAttributesDict[key]?.type === 'IMAGE') {
        return (
          <LabelizedField
            key={key}
            label={key.replaceAll('_i_f', '').replace(/_/g, ' ')}
          >
            <Image src={value} />
          </LabelizedField>
        );
      }
      if (
        flexAttributesDict[key]?.type === 'SELECT_MANY' ||
        flexAttributesDict[key]?.type === 'SELECT_ONE'
      ) {
        let newValue =
          flexAttributesDict[key].choices.find((item) => item.value === value)
            ?.labelEn || '-';
        if (value instanceof Array) {
          newValue = value
            .map(
              (choice) =>
                flexAttributesDict[key].choices.find(
                  (item) => item.value === choice,
                )?.labelEn || '-',
            )
            .join(', ');
        }
        return (
          <LabelizedField
            key={key}
            label={key.replaceAll('_i_f', '').replace(/_/g, ' ')}
            value={newValue}
          />
        );
      }
      return (
        <LabelizedField
          key={key}
          label={key.replaceAll('_i_f', '').replace(/_/g, ' ')}
          value={value}
        />
      );
    },
  );
  return (
    <div>
      <Overview>
        <Title>
          <Typography variant='h6'>{t('Vulnerabilities')}</Typography>
        </Title>
        <Grid container spacing={6}>
          {fields.map((field) => (
            <Grid item xs={4}>
              {field}
            </Grid>
          ))}
        </Grid>
      </Overview>
    </div>
  );
}
