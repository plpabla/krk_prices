import React from "react";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import FlatEstimationForm from "./components/FlatEstimationForm";

const theme = createTheme({
  palette: {
    primary: {
      main: "#40B54D", // Green color from the screenshot
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <FlatEstimationForm />
    </ThemeProvider>
  );
}

export default App;
