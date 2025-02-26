import { TextField, Grid, Select, MenuItem } from "@mui/material";

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
