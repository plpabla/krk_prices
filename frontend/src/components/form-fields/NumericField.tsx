import { Grid, TextField } from "@mui/material";

interface FormFieldProps {
  value: number | null;
  label: string;
  name: string;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function NumericField({
  label,
  value,
  name,
  handleChange,
}: FormFieldProps) {
  return (
    <Grid container spacing={2} sx={{ paddingTop: 4 }}>
      {/* <ResponsiveLabel text="Powierzchnia" /> */}
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
    </Grid>
  );
}
