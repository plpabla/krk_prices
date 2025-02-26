import { TextField, Grid, Select, MenuItem } from "@mui/material";
import { FormData } from "@/types/form";

export interface FormFieldProps {
  formValues: FormData;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function ResponsiveLabel({ text }: { text: string }) {
  return (
    <Grid
      item
      xs={12}
      sm={2}
      container
      alignItems="center"
      justifyContent={{ xs: "flex-start", sm: "flex-end" }}
    >
      {text}
    </Grid>
  );
}
