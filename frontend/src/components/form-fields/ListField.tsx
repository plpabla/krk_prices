import {
  Grid,
  FormControl,
  Select,
  InputLabel,
  MenuItem,
  fabClasses,
} from "@mui/material";
import { FormFieldProps } from "@/components/form-fields/Common";

interface ListFieldProps extends FormFieldProps {
  value: string | null;
  options: {
    [key: string]: string | number;
  };
}

export default function ListField({
  label,
  value,
  name,
  options,
  handleChange,
}: ListFieldProps) {
  return (
    <Grid item xs={12} sm={3}>
      <FormControl fullWidth>
        <InputLabel id={label}>{label}</InputLabel>
        <Select
          value={value || ""}
          labelId={label}
          label={label}
          name={name}
          // @ts-ignore
          onChange={handleChange}
        >
          {Object.entries(options).map(([key, value]) => (
            <MenuItem key={value} value={value}>
              {value}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Grid>
  );
}
