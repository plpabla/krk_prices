import { Grid, FormControl, Select, InputLabel, MenuItem } from "@mui/material";
import { FormFieldProps } from "@/components/form-fields/Common";

interface ListFieldProps extends FormFieldProps {
  value: string | null;
}

export default function ListField({
  label,
  value,
  name,
  handleChange,
}: ListFieldProps) {
  return (
    <Grid item xs={12} sm={3}>
      <FormControl fullWidth>
        <InputLabel id={label}>{label}</InputLabel>
        <Select
          value={value}
          labelId={label}
          label={label}
          name={name}
          // @ts-ignore
          onChange={handleChange}
        >
          <MenuItem value={10}>todo1</MenuItem>
          <MenuItem value={20}>todo2</MenuItem>
          <MenuItem value={30}>todo3</MenuItem>
        </Select>
      </FormControl>
    </Grid>
  );
}
