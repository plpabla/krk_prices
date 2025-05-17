import React from "react";
import { Paper, Typography } from "@mui/material";

const Footer: React.FC = () => {
  return (
    <>
      {/* Spacer to make the form not stick to the bottom */}
      <div style={{ marginBottom: "100px" }} />
      <Paper
        component="footer"
        sx={{
          position: "fixed",
          bottom: 0,
          left: 0,
          right: 0,
          py: 2,
          textAlign: "center",
          backgroundColor: "primary.main",
          color: "white",
          mt: 4,
        }}
      >
        <Typography variant="body2">
          © {new Date().getFullYear()} Wycena Mieszkań. Wszelkie prawa
          zastrzeżone.
        </Typography>
      </Paper>
    </>
  );
};

export default Footer;
