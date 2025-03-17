import { Grid, TextField } from "@mui/material";
import { FormFieldProps } from "@/components/form-fields/Common";

interface NumericFieldProps extends FormFieldProps {
  value: number | null;
}

export default function NumericField({
  label,
  value,
  name,
  handleChange,
}: NumericFieldProps) {
  return (
    <Grid item xs={12} sm={3}>
      <TextField
        label={label}
        id={name}
        name={name}
        value={value || ""}
        onChange={handleChange}
        type="number"
        InputLabelProps={{ shrink: true }}
        sx={{ width: "100%" }}
      />
    </Grid>
  );
}
