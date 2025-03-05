import { Grid } from "@mui/material";
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
      TODO
    </Grid>
  );
}
