import React, { useState } from 'react';
import { client_private } from '../config/client';
import { MemeURLsResponse, UploadMemeResponse } from '../config/types';

const PrivateMemes: React.FC = () => {
  const [memeUrls, setMemeUrls] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const fetchMemeUrls = async () => {
    try {
      const response = await client_private.get<MemeURLsResponse>('/api/v1/meme/urls');
      setMemeUrls(response.data.urls);
    } catch (error) {
      console.error('Error fetching meme URLs:', error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      console.error('No file selected.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await client_private.post<UploadMemeResponse>('/api/v1/meme/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Meme uploaded:', response.data);
      // Optionally update the memeUrls state to include the newly uploaded URL
      fetchMemeUrls(); // Refresh the list of URLs after upload
    } catch (error) {
      console.error('Error uploading meme:', error);
    }
  };

  return (
    <div>
      <h2>Private Meme URLs</h2>
      <button onClick={fetchMemeUrls}>Fetch Meme URLs</button>
      <ul>
        {memeUrls.map((url, index) => (
          <li key={index}>
            <a href={url} target="_blank" rel="noopener noreferrer">{url}</a>
          </li>
        ))}
      </ul>
      <div>
        <input type="file" accept=".jpg,.jpeg,.png,.gif,.bmp,.webp,.tiff" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload Meme</button>
      </div>
    </div>
  );
};

export default PrivateMemes;