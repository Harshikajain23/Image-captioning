import React, { useState } from "react";
import axios from "axios";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [caption, setCaption] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
    setCaption("");
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      alert("Please select an image first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("image", selectedImage);

    try {
      const res = await axios.post(
        "http://localhost:5000/generate_caption",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setCaption(res.data.caption);
    } catch (error) {
      console.error(error);
      alert("Error generating caption!");
    }
    setLoading(false);
  };

  return (
    <div className="bg-gradient-to-r from-purple-200 via-pink-200 to-yellow-200 flex flex-col items-center justify-center h-[100vh] ">
    <div className="min-h-[80vh] min-w-[60vw] bg-white  flex flex-col items-center p-6">
      <h1 className="text-4xl top-[-12px] font-bold text-gray-800 mt-[-6] mb-6">Image Caption Generator</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        className="block w-full max-w-xs text-gray-700 file:bg-purple-300 file:text-black file:px-4 file:py-2 file:rounded-lg file:border-none file:cursor-pointer mt-[-10] mb-4"
      />

      
      {selectedImage && (
        <div className="mt-[-8]">
          <img
            src={URL.createObjectURL(selectedImage)}
            height={400}
            width = {300}
            alt="Uploaded"
            className="mt-[-10] rounded-lg shadow-lg max-w-xs sm:max-w-md mx-auto top-2"
          />
        </div>
      )}
{selectedImage && (
  <button
    onClick={handleUpload}
    className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition duration-300 mt-4"
  >
    {loading ? "Generating..." : "Generate Caption"}
  </button>
)}


      {caption && (
        <div className="mt-[-6] bg-white p-4 rounded-lg shadow-md  text-center text-lg font-medium text-gray-800">
          <span className="font-bold">Caption:</span> {caption}
        </div>
      )}
    </div>

    </div>
  );
}

export default App;