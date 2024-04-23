import { Box, Checkbox, Collapse, Grid, IconButton } from '@mui/material';
import { ArrowDropDown, ArrowRight } from '@mui/icons-material';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { TreeItem, SimpleTreeView } from '@mui/x-tree-view';
import { Field } from 'formik';
import * as React from 'react';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { AllAreasTreeQuery, UserPartnerChoicesQuery } from '@generated/graphql';
import { FormikRadioGroup } from '@shared/Formik/FormikRadioGroup';
import { FormikSelectField } from '@shared/Formik/FormikSelectField';
import { DividerLine } from '@core/DividerLine';
import { DeleteProgramPartner } from './DeleteProgramPartner';
import { AreaTreeNode } from './AreaTreeNode';
import { LabelizedField } from '@components/core/LabelizedField';

interface ProgramPartnerCardProps {
  values;
  partner;
  index: number;
  arrayHelpers;
  allAreasTreeData: AllAreasTreeQuery['allAreasTree'];
  partnerChoices: UserPartnerChoicesQuery['userPartnerChoices'];
  setFieldValue;
}

const BiggestText = styled(Box)`
  font-size: 18px;
  font-weight: 400;
`;

const BigText = styled(Box)`
  font-size: 16px;
  font-weight: 400;
`;

const SmallText = styled(Box)`
  font-size: 14px;
  font-weight: 400;
  color: #49454f;
`;

export const ProgramPartnerCard: React.FC<ProgramPartnerCardProps> = ({
  values,
  partner,
  index,
  arrayHelpers,
  allAreasTreeData,
  partnerChoices,
  setFieldValue,
}): React.ReactElement => {
  const { t } = useTranslation();
  const [isAdminAreaExpanded, setIsAdminAreaExpanded] = useState(false);

  const [allAreasTree, setAllAreasTree] = React.useState<AreaTreeNode[]>(() =>
    AreaTreeNode.buildTree(
      allAreasTreeData,
      values.partners[index]?.adminAreas,
    ),
  );
  const businessAreaOptionLabel = (
    <Box display="flex" flexDirection="column">
      <BigText>{t('Business Area')}</BigText>
      <SmallText>
        {t('The partner has access to the entire business area')}
      </SmallText>
    </Box>
  );

  const handleCheckBoxSelect = (_event, node): void => {
    _event.stopPropagation();
    node.toggleCheck();
    setFieldValue(
      `partners[${index}].adminAreas`,
      AreaTreeNode.getAllSelectedIds(allAreasTree),
    );
    setFieldValue(`partners[${index}].areaAccess`, 'ADMIN_AREA');
    setAllAreasTree([...allAreasTree]);
  };

  const renderNode = (node: AreaTreeNode): React.ReactElement => (
    <TreeItem
      key={node.id}
      itemId={node.id}
      label={
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Checkbox
            id={node.id}
            color="primary"
            checked={Boolean(node.checked)}
            indeterminate={node.checked === 'indeterminate'}
            onChange={(event) => handleCheckBoxSelect(event, node)}
            onClick={(event) => event.stopPropagation()}
          />
          {node.name}
        </div>
      }
    >
      {node.children.length > 0 && node.children.map(renderNode)}
    </TreeItem>
  );

  function groupAreasByLevel(areas, selectedAreas, level = 1) {
    const grouped = { [level]: 0 };

    areas.forEach((area) => {
      if (selectedAreas.includes(area.id)) {
        grouped[level]++;
      }

      if (area.areas && area.areas.length > 0) {
        const subGrouped = groupAreasByLevel(
          area.areas,
          selectedAreas,
          level + 1,
        );
        Object.keys(subGrouped).forEach((key) => {
          if (grouped[key]) {
            grouped[key] += subGrouped[key];
          } else {
            grouped[key] = subGrouped[key];
          }
        });
      }
    });

    return grouped;
  }

  // Get selected admin areas
  const selectedAdminAreas = values.partners[index]?.adminAreas || [];

  // Group allAreasTreeData by level
  const allAreasTreeDataGroupedByLevel = groupAreasByLevel(
    allAreasTreeData,
    selectedAdminAreas,
  );

  const adminAreaOptionLabel = (
    <Box display="flex" flexDirection="column">
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <BigText>{t('Admin Area')}</BigText>
          <SmallText>
            {t(
              "The partner will have access to the program's selected admin area(s):",
            )}
          </SmallText>
          {!isAdminAreaExpanded &&
            Object.values(allAreasTreeDataGroupedByLevel).some(
              (count) => count > 0,
            ) && (
              <Grid container>
                {Object.keys(allAreasTreeDataGroupedByLevel).map((level) => (
                  <Grid key={level} item xs={4}>
                    <LabelizedField
                      dataCy={`Admin-Areas-${level}-field`}
                      label={`Admin Areas ${level}`}
                      key={level}
                    >
                      {allAreasTreeDataGroupedByLevel[level]}
                    </LabelizedField>
                  </Grid>
                ))}
              </Grid>
            )}
        </Box>
        <IconButton
          onClick={() => {
            setIsAdminAreaExpanded(!isAdminAreaExpanded);
          }}
        >
          {isAdminAreaExpanded ? <ArrowDropDown /> : <ArrowRight />}
        </IconButton>
      </Box>
      <Collapse in={isAdminAreaExpanded}>
        <Box style={{ maxHeight: '30vh', overflow: 'auto', width: '50%' }}>
          <SimpleTreeView
            slots={{
              expandIcon: ChevronRightIcon,
              collapseIcon: ExpandMoreIcon,
            }}
            multiSelect
            selectedItems={(values.partners[index]?.adminAreas || []).map(
              String,
            )}
          >
            {allAreasTree.length > 0 && allAreasTree.map(renderNode)}
          </SimpleTreeView>
        </Box>
      </Collapse>
    </Box>
  );

  const handleDeleteProgramPartner = (): void => {
    const foundIndex = values.partners.findIndex((p) => p.id === partner.id);
    if (foundIndex !== -1) {
      arrayHelpers.remove(foundIndex);
    }
  };

  const clearChecks = (): void => {
    allAreasTree.forEach((node) => node.clearChecks());
    setAllAreasTree([...allAreasTree]);
  };

  return (
    <Grid container direction="column">
      <Box display="flex" justifyContent="space-between">
        <Grid item xs={6}>
          <Field
            name={`partners[${index}].id`}
            label={t('Partner')}
            color="primary"
            choices={partnerChoices}
            component={FormikSelectField}
          />
        </Grid>
        <DeleteProgramPartner
          // TODO: add permission
          canDeleteProgramPartner
          handleDeleteProgramPartner={handleDeleteProgramPartner}
        />
      </Box>
      <Box mt={2}>
        <BiggestText>{t('Area Access')}</BiggestText>
      </Box>
      <Grid item xs={6}>
        <Field
          name={`partners[${index}].areaAccess`}
          required={values.partners[index]?.id !== ''}
          choices={[
            {
              value: 'BUSINESS_AREA',
              name: t('Business Area'),
              optionLabel: businessAreaOptionLabel,
            },
            {
              value: 'ADMIN_AREA',
              name: t('Admin Area'),
              optionLabel: adminAreaOptionLabel,
            },
          ]}
          component={FormikRadioGroup}
          withGreyBox
          onChange={(event) => {
            setIsAdminAreaExpanded(event.target.value === 'ADMIN_AREA');
            if (event.target.value === 'BUSINESS_AREA') {
              setFieldValue(`partners[${index}].adminAreas`, []);
              clearChecks();
            }
          }}
        />
      </Grid>
      {index + 1 < values.partners.length && <DividerLine />}
    </Grid>
  );
};
