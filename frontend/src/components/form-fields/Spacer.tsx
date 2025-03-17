import { Grid } from "@mui/material";

export default function Spacer({ n = 1 }: { n?: number }) {
  return (
    <Grid item xs={12} sm={3 * n}>
      {/* This is an intentionally empty grid item for spacing */}
    </Grid>
  );
}
