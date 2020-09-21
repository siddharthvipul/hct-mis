import { Avatar, Box, Button, Grid, Typography } from '@material-ui/core';
import { Field, Form, Formik } from 'formik';
import React from 'react';
import styled from 'styled-components';
import { FormikTextField } from '../../shared/Formik/FormikTextField';
import { UniversalMoment } from '../UniversalMoment';

export function Notes(): React.ReactElement {
  const Container = styled.div`
    display: flex;
    flex: 1;
    width: 100%;
    background-color: #fff;
    padding: ${({ theme }) => theme.spacing(8)}px
      ${({ theme }) => theme.spacing(11)}px;
    flex-direction: column;
    border-color: #b1b1b5;
    border-bottom-width: 1px;
    border-bottom-style: solid;
  `;
  const OverviewContainer = styled.div`
    display: flex;
    align-items: center;
    flex-direction: column;
  `;

  const Title = styled.div`
    padding-bottom: ${({ theme }) => theme.spacing(8)}px;
  `;
  const Name = styled.span`
    font-size: 16px;
  `;
  const Date = styled.span`
    font-size: 12px;
    color: #848484;
  `;
  const DescMargin = styled.div`
    margin-bottom: 35px;
  `;

  const note = (
    avatar: string,
    name: string,
    date: string,
    description: string,
  ): React.ReactElement => (
    <Grid container>
      <Grid item xs={2}>
        <Avatar src={avatar} alt={`${name} picture`} />
      </Grid>
      <Grid item xs={10}>
        <Grid item xs={12}>
          <Box display='flex' justifyContent='space-between'>
            <Name>{name}</Name>
            <Date>{date}</Date>
          </Box>
        </Grid>
        <Grid item xs={12}>
          <DescMargin>
            <p>{description}</p>
          </DescMargin>
        </Grid>
      </Grid>
    </Grid>
  );
  const d = new window.Date();
  const now = <UniversalMoment withTime>{`${d}`}</UniversalMoment>;

  const mappedNotes = [
    {
      name: 'Martin Scott',
      avatar: 'picture',
      date: '07/15/2020, 4:46 PM',
      description: 'Lorem lorem lorem ipsum',
    },
    {
      name: 'Ben Johnson',
      avatar: 'picture',
      date: '02/10/2020, 4:46 PM',
      description: 'Lorem lorem lorem ipsum',
    },
  ].map((el) => note(el.avatar, el.name, el.date, el.description));

  const initialValues: { [key: string]: string } = {
    newNote: '',
  };

  return (
    <Formik
      initialValues={initialValues}
      onSubmit={(values) => {
        console.log(values);
      }}
      // validationSchema={validationSchema}
    >
      {({ submitForm, values }) => (
        <Container>
          <Title>
            <Typography variant='h6'>Notes</Typography>
          </Title>
          <OverviewContainer>
            {mappedNotes}
            <Grid container>
              <Grid item xs={2}>
                <Avatar src='me' alt={`${'me'} picture`} />
              </Grid>
              <Grid item xs={10}>
                <Grid item xs={12}>
                  <Box display='flex' justifyContent='space-between'>
                    <Name>My name</Name>
                  </Box>
                </Grid>
                <Grid item xs={12}>
                  <DescMargin>
                    <Form>
                      <Field
                        name='newNote'
                        multiline
                        fullWidth
                        variant='filled'
                        label='Add a note ...'
                        component={FormikTextField}
                      />
                      <Box mt={2} display='flex' justifyContent='flex-end'>
                        <Button
                          color='primary'
                          variant='contained'
                          onClick={submitForm}
                        >
                          Add New Note
                        </Button>
                      </Box>
                    </Form>
                  </DescMargin>
                </Grid>
              </Grid>
            </Grid>
          </OverviewContainer>
        </Container>
      )}
    </Formik>
  );
}
