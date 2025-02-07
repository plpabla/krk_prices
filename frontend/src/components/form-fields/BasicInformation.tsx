import React from "react";
import { TextField, Grid, InputAdornment } from "@mui/material";
import { FormData } from "@/types/form";

interface BasicInformationProps {
  formData: FormData;
  onTextChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onNumberChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const BasicInformation: React.FC<BasicInformationProps> = ({
  formData,
  onTextChange,
  onNumberChange,
}) => {
  return (
    <>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Nazwa ogłoszenia"
          name="name"
          value={formData.name}
          onChange={onTextChange}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Powierzchnia"
          name="area"
          type="number"
          value={formData.area ?? ""}
          onChange={onNumberChange}
          InputProps={{
            endAdornment: <InputAdornment position="end">m²</InputAdornment>,
          }}
        />
      </Grid>
    </>
  );
};

export default BasicInformation;
