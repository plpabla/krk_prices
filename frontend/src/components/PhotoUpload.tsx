import { useRef, useState } from "react";
import { Formik, Form, FormikHelpers } from "formik";

import { uploadPhotos } from "@/api";
import PhotoFeedback from "./PhotoFeedback";
import { PhotoFeedbackProps, defaultPhotoFeedbackProps } from "./PhotoFeedback";

interface FormValues {
  files: File[];
}

export default function PhotoUpload() {
  const [imgSrc, setImgSrc] = useState<string[]>([]);
  const [processed, setProcessed] = useState<boolean>(false);
  const [photoFeedback, setPhotoFeedback] = useState<PhotoFeedbackProps>(
    defaultPhotoFeedbackProps
  );
  const fileRef = useRef<HTMLInputElement>(null);

  const displayFiles = (files: File[]) => {
    setImgSrc([]);
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImgSrc((prev) => [...prev, reader.result as string]);
      };
      reader.readAsDataURL(file);
    });
  };

  const initialValues: FormValues = {
    files: [],
  };

  const handleSubmit = (
    values: FormValues,
    { setSubmitting }: FormikHelpers<FormValues>
  ) => {
    if (values.files.length > 0) {
      setSubmitting(true);
      uploadPhotos(values.files)
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
              id="files"
              name="files"
              type="file"
              accept="image/*"
              ref={fileRef}
              multiple
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  const filesArray = Array.from(e.target.files);
                  setFieldValue("files", filesArray);
                  displayFiles(filesArray);
                  setProcessed(false);
                }
              }}
            />
            <div>
              {imgSrc.map((src, index) => (
                <img
                  key={index}
                  src={src}
                  alt={`Preview ${index + 1}`}
                  width="30%"
                  style={{ margin: "5px" }}
                />
              ))}
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
