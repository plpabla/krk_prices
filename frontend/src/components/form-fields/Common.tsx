import { Grid } from "@mui/material";

export interface FormFieldProps {
  value: any;
  label: string;
  name: string;
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
