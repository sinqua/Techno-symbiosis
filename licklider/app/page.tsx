'use client'
import React, { useEffect, useState } from "react";

export default function Home() {

  // enter your server ip address
  const serverUrl = "http://192.168.45.187:8080";

  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [inputText, setInputText] = useState<string>("");
  const [fetchedText, setFetchedText] = useState<string>("");
  const [isSending, setIsSending] = useState<boolean>(false);

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

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(event.target.value);
    event.target.style.height = "inherit";
    event.target.style.height = `${event.target.scrollHeight}px`;
  };

  const handleSendText = async () => {
    setIsSending(true);
    const formData = new FormData();
    formData.append("text", inputText);

    const response = await fetch(`${serverUrl}/text`, {
      method: "POST",
      body: formData,
      mode: "cors",
    });

    if (response.ok) {
      const data = await response.text();
      setFetchedText(data);
    }
    else {
      setFetchedText("Error");
    }
    setIsSending(false);
  }

  const handleSendImage = async () => {
    setIsSending(true);
    const formData = new FormData();
    formData.append("image", selectedImage as Blob);

    const response = await fetch(`${serverUrl}/image`, {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.text();
      setFetchedText(data);
    }
    else {
      setFetchedText("Error");
    }
    setIsSending(false);
  }

  const handleGetHistory = async () => {

    fetch(`${serverUrl}/history`, {
      method: "GET",
    }).then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
}

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-10 dark:bg-gray-900 dark:text-white">
      <div className="flex flex-col z-10 w-full max-w-md mx-auto justify-between font-mono text-sm lg:flex">
        <h1 className="text-3xl font-bold mb-10">Postman</h1>
        <h2 className="text-xl font-bold mb-3">편지쓰기</h2>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        {imageSrc && <img src={imageSrc} alt="Selected" />}
        <button className="w-full h-8 mt-5 mb-5 bg-blue-500 border border-black dark:bg-blue-700 dark:border-white" onClick={handleSendImage} disabled={isSending}>
          {isSending ? "전송 중..." : "전송"}
        </button>
        <h2 className="text-xl font-bold mb-3">말하기</h2>
        <textarea className="w-full overflow-visible dark:text-black" value={inputText} onChange={handleTextChange} />
        <button className="w-full h-8 mt-5 mb-5 bg-blue-500 border border-black dark:bg-blue-700 dark:border-white" onClick={handleSendText} disabled={isSending}>
          {isSending ? "전송 중..." : "전송"}
        </button>
        <h2 className="text-xl font-bold mb-3">대답</h2>
        <p>{fetchedText}</p>
        <button className="w-full h-8 mt-5 mb-5 bg-blue-500 border border-black dark:bg-blue-700 dark:border-white" onClick={handleGetHistory} disabled={isSending}>
          대화기록
        </button>
      </div>
    </main>
  );
}
