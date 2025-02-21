import React from "react";
import { TextField, Grid, InputAdornment } from "@mui/material";
import { FormData } from "@/types/form";
import Location from "./Location";

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
      <Location formData={formData} onTextChange={onTextChange} />
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
