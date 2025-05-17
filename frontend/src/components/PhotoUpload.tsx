import { useRef, useState } from "react";
import { Formik, Form, FormikHelpers } from "formik";

import { uploadPhoto } from "@/api";
import PhotoFeedback from "./PhotoFeedback";
import { PhotoFeedbackProps, defaultPhotoFeedbackProps } from "./PhotoFeedback";

interface FormValues {
  file: File | null;
}

export default function PhotoUpload() {
  const [imgSrc, setImgSrc] = useState<string>("");
  const [processed, setProcessed] = useState<boolean>(false);
  const [photoFeedback, setPhotoFeedback] = useState<PhotoFeedbackProps>(
    defaultPhotoFeedbackProps
  );
  const fileRef = useRef<HTMLInputElement>(null);

  const displayFile = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setImgSrc(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const initialValues: FormValues = {
    file: null,
  };

  const handleSubmit = (
    values: FormValues,
    { setSubmitting }: FormikHelpers<FormValues>
  ) => {
    if (values.file) {
      const formData = new FormData();
      formData.append("file", values.file);

      uploadPhoto(values.file)
        .then((res) => {
          console.log(">>>", res);
          const photoFeedbackData: PhotoFeedbackProps = {
            luxuryLevel: parseInt(res.luxury_level, 10),
            type: res.type,
            pros: res.pros,
            to_fix: res.to_fix,
            description: res.description,
          };
          setPhotoFeedback(photoFeedbackData);
          setProcessed(true);
        })
        .catch((error) => {
          console.error("Error uploading photo:", error);
          alert("Wystąpił błąd podczas przesyłania zdjęcia.");
        })
        .finally(() => {
          setSubmitting(false);
        });
    } else {
      alert("Proszę wybrać zdjęcie.");
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h1>Wczytaj zdjęcie</h1>
      <Formik initialValues={initialValues} onSubmit={handleSubmit}>
        {({ setFieldValue, isSubmitting }) => (
          <Form>
            <input
              id="file"
              name="file"
              type="file"
              accept="image/*"
              ref={fileRef}
              onChange={(e) => {
                if (e.target.files) {
                  const file = e.target.files[0];
                  setFieldValue("file", file);
                  displayFile(file);
                  setProcessed(false);
                }
              }}
            />
            <div>
              {imgSrc && <img src={imgSrc} alt="Preview" width="100%" />}
            </div>
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Wysyłanie..." : "Wyślij"}
            </button>
          </Form>
        )}
      </Formik>

      {processed && <PhotoFeedback {...photoFeedback} />}
    </div>
  );
}
