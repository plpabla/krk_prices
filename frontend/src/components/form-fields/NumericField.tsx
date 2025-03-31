import { Grid, TextField } from "@mui/material";
import { FormFieldProps } from "@/components/form-fields/Common";
import { useState } from "react";

interface NumericFieldProps extends FormFieldProps {
  value: number | null;
}

export default function NumericField({
  label,
  value,
  name,
  handleChange,
}: NumericFieldProps) {
  const [touched, setTouched] = useState<boolean>(false);

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
        required
        error={value === null && touched}
        helperText={value === null && touched ? "To pole jest wymagane" : ""}
        onBlur={() => {
          if (!touched) {
            setTouched(true);
          }
        }}
      />
    </Grid>
  );
}
