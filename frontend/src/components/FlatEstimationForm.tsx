import React from "react";
import { useState, useEffect, useRef } from "react";
import { Formik } from "formik";
import { useNavigate } from "react-router-dom";

import { useFormStore } from "@/state/formData";
import { getPriceEstimate } from "@/api";
import FormText from "@/components/FormText";
import FormImages, { displayFiles } from "@/components/FormImages";
import Submit from "@/components/form-fields/Submit";
import Loading from "@/components/Loading";
import { FormData } from "@/types/form";

const FlatEstimationForm: React.FC = () => {
  const navigate = useNavigate();
  const { formData, setFormData } = useFormStore();
  const [processing, setProcessing] = useState<boolean>(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const [imgSrc, setImgSrc] = useState<string[]>([]);

  useEffect(() => {
    displayFiles(setImgSrc, formData.files);
  }, []);

  const handleSubmit = (values: FormData) => {
    setProcessing(true);
    setFormData(values);
    getPriceEstimate({ ...values })
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
    return <Loading />;
  }

  return (
    <>
      <h1>Darmowa wycena mieszkań</h1>
      <Formik initialValues={formData} onSubmit={handleSubmit}>
        {({ values, handleChange, handleSubmit, setFieldValue }) => (
          <form onSubmit={handleSubmit}>
            <FormText
              handleChange={handleChange}
              values={values}
              formData={formData}
            />
            <FormImages
              setFieldValue={setFieldValue}
              fileRef={fileRef}
              imgSrc={imgSrc}
              setImgSrc={setImgSrc}
            />
            <Submit disabled={processing} />
          </form>
        )}
      </Formik>
    </>
  );
};

export default FlatEstimationForm;
