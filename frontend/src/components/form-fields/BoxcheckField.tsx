import { Grid, Checkbox, FormControlLabel } from "@mui/material";

export default function BoxcheckField() {
  return (
    <Grid item xs={12} sm={3}>
      <FormControlLabel
        control={<Checkbox />}
        label="Check me"
        sx={{ width: "100%" }}
      />
    </Grid>
  );
}
