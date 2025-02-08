import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import FlatEstimationForm from "./components/FlatEstimationForm";

const theme = createTheme({
  palette: {
    primary: {
      main: "#40B54D",
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
