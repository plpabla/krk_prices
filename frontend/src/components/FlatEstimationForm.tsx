import React from "react";
import { Formik } from "formik";
import { Container, Grid } from "@mui/material";

import { defaultFormData } from "@/types/form";
import { getPriceEstimate } from "@/api";
import Submit from "@/components/form-fields/Submit";
import Location from "@/components/form-fields/Location";
import NumericField from "@/components/form-fields/NumericField";
import BoxcheckField from "@/components/form-fields/BoxcheckField";

const FlatEstimationForm: React.FC = () => {
  return (
    <>
      <Container className="m-10">
        <h1>Darmowa wycena mieszkań</h1>
        <Formik
          initialValues={defaultFormData}
          onSubmit={(values, { setSubmitting }) => {
            setTimeout(() => {
              getPriceEstimate(values).then((price) => {
                console.log("Price estimate:", price);
              });
              setSubmitting(false);
            }, 400);
          }}
        >
          {({ values, handleChange, handleSubmit }) => (
            <form onSubmit={handleSubmit}>
              <Location handleChange={handleChange} formValues={values} />
              <Grid container spacing={2} sx={{ paddingTop: 4 }}>
                <NumericField
                  label="Powierzchnia [m²]"
                  name="area"
                  value={values.area}
                  handleChange={handleChange}
                />
                <NumericField
                  label="Liczba pokoi"
                  name="rooms"
                  value={values.rooms}
                  handleChange={handleChange}
                />
                <NumericField
                  label="Piętro"
                  name="floor"
                  value={values.floor}
                  handleChange={handleChange}
                />
                <NumericField
                  label="Ilość pięter w budynku"
                  name="floorsInBuilding"
                  value={values.floorsInBuilding}
                  handleChange={handleChange}
                />
                <BoxcheckField
                  label="taras/balkon"
                  name="balcony"
                  value={values.balcony}
                  handleChange={handleChange}
                />
              </Grid>
              <Submit />
            </form>
          )}
        </Formik>
      </Container>
    </>
  );
};

export default FlatEstimationForm;
