import React from "react";
import { Grid } from "@mui/material";
import { FormData } from "@/types/form";
import BasicInformation from "./form-fields/BasicInformation";
import RoomDetails from "./form-fields/RoomDetails";
import PropertyDetails from "./form-fields/PropertyDetails";
import OwnershipDetails from "./form-fields/OwnershipDetails";
import AdditionalDetails from "./form-fields/AdditionalDetails";

interface FormFieldsProps {
  formData: FormData;
  onChange: (name: string, value: string | number | null) => void;
}

const FormFields: React.FC<FormFieldsProps> = ({ formData, onChange }) => {
  const handleTextChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    onChange(event.target.name, event.target.value);
  };

  const handleNumberChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    const numericValue = value === "" ? null : Number(value);
    onChange(name, numericValue);
  };

  const handleSelectChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.name, event.target.value);
  };

  return (
    <Grid container spacing={3}>
      <BasicInformation
        formData={formData}
        onTextChange={handleTextChange}
        onNumberChange={handleNumberChange}
      />

      <RoomDetails formData={formData} onNumberChange={handleNumberChange} />

      <PropertyDetails
        formData={formData}
        onSelectChange={handleSelectChange}
      />

      <OwnershipDetails
        formData={formData}
        onSelectChange={handleSelectChange}
      />

      <AdditionalDetails
        formData={formData}
        onTextChange={handleTextChange}
        onNumberChange={handleNumberChange}
      />
    </Grid>
  );
};

export default FormFields;
