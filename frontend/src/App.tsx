import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { Container } from "@mui/material";

import FlatEstimationForm from "@/components/FlatEstimationForm";
import PriceEstimationPage from "@/components/PriceEstimationPage";
import Footer from "@/components/Footer";
import Navbar from "./components/Navbar";

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
      <Container className="m-10">
        <Navbar />
        <Routes>
          <Route path="/" element={<FlatEstimationForm />} />
          <Route path="/estimate" element={<PriceEstimationPage />} />
        </Routes>
        <Footer />
      </Container>
    </ThemeProvider>
  );
}

export default App;
