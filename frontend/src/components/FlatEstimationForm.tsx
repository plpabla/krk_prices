import React from "react";
import { Box, Button, Typography, Container, Grid } from "@mui/material";
import { FormData, defaultFormData } from "@/types/form";
import Location from "@/components/form-fields/Location";

const FlatEstimationForm: React.FC = () => {
  return (
    <>
      <Container className="m-10">
        <h1>Darmowa wycena mieszkań!</h1>
        <Location />
      </Container>
    </>
  );
};

export default FlatEstimationForm;
