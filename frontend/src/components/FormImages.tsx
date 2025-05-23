type FormImagesProps = {
  setFieldValue: (field: string, value: any) => void;
  fileRef: React.RefObject<HTMLInputElement>;
  imgSrc: string[];
  setImgSrc: React.Dispatch<React.SetStateAction<string[]>>;
};

type setterFnType = React.Dispatch<React.SetStateAction<string[]>>;

export const displayFiles = (setterFn: setterFnType, files: File[]) => {
  setterFn([]);
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setterFn((prev) => [...prev, reader.result as string]);
    };
    reader.readAsDataURL(file);
  });
};

export default function FormImages({
  fileRef,
  setFieldValue,
  imgSrc,
  setImgSrc,
}: FormImagesProps) {
  return (
    <>
      <h2>Wczytaj zdjęcia (opcjonalnie)</h2>
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
            displayFiles(setImgSrc, filesArray);
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
    </>
  );
}
