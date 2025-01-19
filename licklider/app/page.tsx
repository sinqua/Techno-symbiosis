'use client'
import React, { useEffect, useState, useRef } from "react";

const App = () => {

  // enter your server ip address
  const serverUrl = "http://192.168.219.104:8080";

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [inputText, setInputText] = useState<string>("");
  const [fetchedText, setFetchedText] = useState<string>("");
  const [isSending, setIsSending] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setImageSrc(URL.createObjectURL(file));
    }
  };

  const handleRemoveImage = () => {
    setSelectedImage(null);
    setImageSrc(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(event.target.value);
    event.target.style.height = "inherit";
    event.target.style.height = `${event.target.scrollHeight}px`;
  };

  const handleSend = async () => {
    setIsSending(true);

    let formData = new FormData();
    if (selectedImage) {
      formData.append("image", selectedImage as Blob);
    }
    formData.append("text", inputText);

    const response = await fetch(`${serverUrl}/send`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.text();
      setFetchedText(data);
    } else {
      setFetchedText("Error");
    }
    setIsSending(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-10 dark:bg-gray-900 dark:text-white">
      <div className="flex flex-col z-10 w-full max-w-md mx-auto justify-between font-mono text-sm lg:flex">
        <h1 className="text-3xl font-bold mb-10">Postman</h1>
        <h2 className="text-xl font-bold mb-3">이미지</h2>
        <input type="file" accept="image/*" onChange={handleImageChange} ref={fileInputRef} />
        {imageSrc && (
          <div>
            <img src={imageSrc} alt="Selected" />
            <button className="w-full h-8 mt-2 mb-5 bg-red-500 border border-black dark:bg-red-700 dark:border-white" onClick={handleRemoveImage}>
              이미지 해제
            </button>
          </div>
        )}
        <h2 className="text-xl font-bold mb-3">텍스트</h2>
        <textarea className="w-full overflow-visible dark:text-black" value={inputText} onChange={handleTextChange} />
        <button className="w-full h-8 mt-5 mb-5 bg-blue-500 border border-black dark:bg-blue-700 dark:border-white" onClick={handleSend} disabled={isSending}>
          {isSending ? "전송 중..." : "전송"}
        </button>
        <h2 className="text-xl font-bold mb-3">대답</h2>
        <p>{fetchedText}</p>

      </div>
    </main>
  );
};

export default App;
