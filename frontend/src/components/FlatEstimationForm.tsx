import React from "react";
import { Formik } from "formik";
import { Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { defaultFormData } from "@/types/form";
import {
  StateDict,
  MarketDict,
  AdDict,
  OwnershipDict,
  AvailableDict,
  HeatingDict,
} from "@/types/enums";
import { getPriceEstimate } from "@/api";
import Submit from "@/components/form-fields/Submit";
import Spacer from "@/components/form-fields/Spacer";
import Location from "@/components/form-fields/Location";
import NumericField from "@/components/form-fields/NumericField";
import BoxcheckField from "@/components/form-fields/BoxcheckField";
import ListField from "@/components/form-fields/ListField";

const FlatEstimationForm: React.FC = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>Darmowa wycena mieszkań</h1>
      <Formik
        initialValues={defaultFormData}
        onSubmit={(values, { setSubmitting }) => {
          setTimeout(() => {
            getPriceEstimate(values).then(() => {
              navigate("/estimate", { replace: true });
            });
            setSubmitting(false);
          }, 400);
        }}
      >
        {({ values, handleChange, handleSubmit }) => (
          <form onSubmit={handleSubmit}>
            <Location handleChange={handleChange} formValues={values} />
            <Grid
              container
              spacing={4}
              sx={{ paddingTop: 4, paddingBottom: 4 }}
            >
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
              <BoxcheckField
                label="oddzielna kuchnia"
                name="separate_kitchen"
                value={values.separate_kitchen}
                handleChange={handleChange}
              />
              <ListField
                label="Ogrzewanie"
                name="heating"
                options={HeatingDict}
                value={values.heating}
                handleChange={handleChange}
              />
              <Spacer n={1} />

              <ListField
                label="Rynek"
                name="market"
                options={MarketDict}
                value={values.market}
                handleChange={handleChange}
              />
              <ListField
                label="Typ ogłoszenia"
                name="ad_type"
                options={AdDict}
                value={values.ad_type}
                handleChange={handleChange}
              />
              <ListField
                label="Typ własności"
                name="ownership"
                options={OwnershipDict}
                value={values.ownership}
                handleChange={handleChange}
              />
              <Spacer n={1} />

              <ListField
                label="Stan mieszkania"
                name="state"
                options={StateDict}
                value={values.state}
                handleChange={handleChange}
              />
              <ListField
                label="Dostępne od"
                name="available"
                options={AvailableDict}
                value={values.available}
                handleChange={handleChange}
              />
              <Spacer n={2} />
              <BoxcheckField
                label="garaż/miejsce parkingowe"
                name="garage"
                value={values.garage}
                handleChange={handleChange}
              />
              <BoxcheckField
                label="winda"
                name="elevator"
                value={values.elevator}
                handleChange={handleChange}
              />
              <BoxcheckField
                label="piwnica/komórka lokatorska"
                name="basement"
                value={values.basement}
                handleChange={handleChange}
              />
            </Grid>
            <Submit />
          </form>
        )}
      </Formik>
    </>
  );
};

export default FlatEstimationForm;
