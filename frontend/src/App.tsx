import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import FlatEstimationForm from "@/components/FlatEstimationForm";
import Footer from "@/components/Footer";

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
      <Footer />
    </ThemeProvider>
  );
}

export default App;
