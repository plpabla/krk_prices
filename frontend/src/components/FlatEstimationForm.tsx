import React from "react";
import { useState, useEffect, useRef } from "react";
import { Formik } from "formik";
import { Grid } from "@mui/material";
import { useNavigate } from "react-router-dom";

import { useFormStore } from "@/state/formData";
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
import { FormData } from "@/types/form";

const Waiting = () => (
  <div>
    <h2>Przetwarzanie...</h2>
    <p>Proszę czekać, trwa przetwarzanie formularza.</p>
  </div>
);

const FlatEstimationForm: React.FC = () => {
  const navigate = useNavigate();
  const { formData, setFormData } = useFormStore();
  const [processing, setProcessing] = useState<boolean>(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const [imgSrc, setImgSrc] = useState<string[]>([]);

  useEffect(() => {
    displayFiles(formData.files);
  }, []);

  const displayFiles = (files: File[]) => {
    setImgSrc([]);
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImgSrc((prev) => [...prev, reader.result as string]);
      };
      reader.readAsDataURL(file);
    });
  };

  const handleSubmit = (values: FormData) => {
    setProcessing(true);
    setFormData(values);
    getPriceEstimate({ ...values, files: [] })
      .then(() => {
        setProcessing(false);
        navigate("/estimate", { replace: true });
      })
      .catch((error) => {
        console.error("Error during form submission:", error);
        alert("Wystąpił błąd podczas przesyłania formularza.");
        setProcessing(false);
      });
  };

  if (processing) {
    return <Waiting />;
  }

  return (
    <>
      <h1>Darmowa wycena mieszkań</h1>
      <Formik initialValues={formData} onSubmit={handleSubmit}>
        {({ values, handleChange, handleSubmit, setFieldValue }) => (
          <form onSubmit={handleSubmit}>
            <Location
              handleChange={handleChange}
              formValues={values}
              defaultDistrict={formData.district}
            />
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
            <h2>Wczytaj zdjęcia (opcjonalnie)</h2>
            <input
              id="files"
              name="files"
              type="file"
              accept="image/*"
              ref={fileRef}
              multiple
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  const filesArray = Array.from(e.target.files);
                  setFieldValue("files", filesArray);
                  displayFiles(filesArray);
                }
              }}
            />
            <div>
              {imgSrc.map((src, index) => (
                <img
                  key={index}
                  src={src}
                  alt={`Preview ${index + 1}`}
                  width="30%"
                  style={{ margin: "5px" }}
                />
              ))}
            </div>
            <Submit disabled={processing} />
          </form>
        )}
      </Formik>
    </>
  );
};

export default FlatEstimationForm;
