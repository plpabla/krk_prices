import { Grid, TextField } from "@mui/material";

import { FormFieldProps } from "@/components/form-fields/Common";

export default function Area({ handleChange, formValues }: FormFieldProps) {
  return (
    <Grid container spacing={2} sx={{ paddingTop: 4 }}>
      {/* <ResponsiveLabel text="Powierzchnia" /> */}
      <Grid item xs={12} sm={3}>
        <TextField
          label="Powierzchnia [m²]"
          id="area"
          name="area"
          value={formValues.area || ""}
          onChange={handleChange}
          type="number"
          InputLabelProps={{ shrink: true }}
          sx={{ width: "100%" }}
        />
      </Grid>
    </Grid>
  );
}
