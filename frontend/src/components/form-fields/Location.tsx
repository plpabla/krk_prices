import React from "react";
import { TextField, Grid } from "@mui/material";
import { FormData } from "@/types/form";

export default function Location() {
  return (
    <>
      <Grid item xs={12}>
        <TextField
          fullWidth
          label="Lokalizacja"
          name="location"
          value={42}
          onChange={() => {}}
        />
      </Grid>
    </>
  );
}
