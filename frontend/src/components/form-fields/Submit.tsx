import { Button, Grid } from "@mui/material";

export default function Submit({ disabled = false }: { disabled?: boolean }) {
  return (
    <Grid item xs={12}>
      <Button
        fullWidth
        type="submit"
        variant="contained"
        color="primary"
        disabled={disabled}
        sx={{ mt: 3, mb: 2 }}
      >
        Wyślij
      </Button>
    </Grid>
  );
}
