'use client'
import React, { useEffect, useState } from "react";

export default function Home() {

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [inputText, setInputText] = useState<string>("");
  const [fetchedText, setFetchedText] = useState<string>("");

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedImage(event.target.files[0]);

      const reader = new FileReader();
      reader.onloadend = () => {
        setImageSrc(reader.result as string);
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };

  const handleSend = async () => {
    const formData = new FormData();
    // formData.append("image", selectedImage as Blob);
    formData.append("text", inputText);

    const response = await fetch("http://localhost:5000", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText }),
    });

    if (response.ok) {
      const data = await response.text();
      setFetchedText(data);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <input type="file" accept="image/*" onChange={handleImageChange} />
        {imageSrc && <img src={imageSrc} alt="Selected" />}
        <input type="text" value={inputText} onChange={handleTextChange} />

        <button onClick={handleSend}>Send</button>
        <p>{fetchedText}</p>
      </div>
    </main>
  );
}
