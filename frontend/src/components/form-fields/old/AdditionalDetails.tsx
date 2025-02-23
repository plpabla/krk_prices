import React from "react";
import { TextField, Grid, InputAdornment } from "@mui/material";
import { FormData } from "@/types/form";

interface AdditionalDetailsProps {
  formData: FormData;
  onTextChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onNumberChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const AdditionalDetails: React.FC<AdditionalDetailsProps> = ({
  formData,
  onTextChange,
  onNumberChange,
}) => {
  return (
    <>
      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Czynsz"
          name="rent"
          type="number"
          value={formData.rent ?? ""}
          onChange={onNumberChange}
          InputProps={{
            endAdornment: <InputAdornment position="end">zł</InputAdornment>,
          }}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <TextField
          fullWidth
          label="Dostępne od"
          name="available"
          type="date"
          value={formData.available}
          onChange={onTextChange}
          InputLabelProps={{
            shrink: true,
          }}
        />
      </Grid>

      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Informacje dodatkowe"
          name="extra_info"
          multiline
          rows={4}
          value={formData.extra_info}
          onChange={onTextChange}
        />
      </Grid>
    </>
  );
};

export default AdditionalDetails;
