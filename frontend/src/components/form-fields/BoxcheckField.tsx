import { Grid, Checkbox, FormControlLabel } from "@mui/material";

interface FormFieldProps {
  value: boolean;
  label: string;
  name: string;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function BoxcheckField({
  value,
  label,
  name,
  handleChange,
}: FormFieldProps) {
  return (
    <Grid item xs={12} sm={3}>
      <FormControlLabel
        control={<Checkbox />}
        label={label}
        name={name}
        checked={!!value}
        // @ts-ignore
        onChange={handleChange}
        sx={{ width: "100%" }}
        inputProps={{ "aria-label": "controlled" }}
      />
    </Grid>
  );
}
