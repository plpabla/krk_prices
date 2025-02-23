import React from "react";
import { Box, Button, Typography, Container, Grid } from "@mui/material";
import { FormData, defaultFormData } from "@/types/form";
import Location from "@/components/form-fields/Location";
import Submit from "@/components/form-fields/Submit";
import { Formik } from "formik";

const FlatEstimationForm: React.FC = () => {
  return (
    <>
      <Container className="m-10">
        <h1>Darmowa wycena mieszkań</h1>
        <Formik
          initialValues={defaultFormData}
          onSubmit={(values, { setSubmitting }) => {
            setTimeout(() => {
              alert(JSON.stringify(values, null, 2));
              setSubmitting(false);
            }, 400);
          }}
        >
          {({ values, errors, touched, handleChange, handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <Location handleChange={handleChange} formValues={values} />
              {errors.location && touched.location && errors.location}
              <Submit />
            </form>
          )}
        </Formik>
      </Container>
    </>
  );
};

export default FlatEstimationForm;
