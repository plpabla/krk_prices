import { Grid, Checkbox, FormControlLabel } from "@mui/material";
import { FormFieldProps } from "@/components/form-fields/Common";

interface BoxcheckFieldProps extends FormFieldProps {
  value: boolean;
}

export default function BoxcheckField({
  value,
  label,
  name,
  handleChange,
}: BoxcheckFieldProps) {
  return (
    <Grid item xs={6} sm={3}>
      <FormControlLabel
        control={<Checkbox />}
        label={label}
        name={name}
        checked={!!value}
        // @ts-ignore
        onChange={handleChange}
        sx={{ width: "100%" }}
      />
    </Grid>
  );
}
