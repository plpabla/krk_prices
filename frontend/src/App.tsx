import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { Routes, Route } from "react-router-dom";

import FlatEstimationForm from "@/components/FlatEstimationForm";
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
      <Navbar />
      <Routes>
        <Route path="/" element={<FlatEstimationForm />} />
        <Route path="/demo" element={<h1>test</h1>} />
      </Routes>
      <Footer />
    </ThemeProvider>
  );
}

export default App;
