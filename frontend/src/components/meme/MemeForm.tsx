import React, { useState } from 'react';
import { client_public } from '../config/client';
import type { MemeForm } from '../config/types';

const MemeForm: React.FC = () => {
  const initialFormState: MemeForm = {
    title: '',
    description: '',
    image_url: '',
  };
  const [formData, setFormData] = useState<MemeForm>(initialFormState);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await client_public.post('/api/v1/meme', formData);
      console.log('Meme created:', response.data);
      setFormData(initialFormState);
    } catch (error) {
      console.error('Error creating meme:', error);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="title"
        value={formData.title}
        onChange={handleChange}
        placeholder="Title"
        required
      />
      <input
        type="text"
        name="description"
        value={formData.description?.toString()}
        onChange={handleChange}
        placeholder="Description"
        required
      />
      <input
        type="text"
        name="image_url"
        value={formData.image_url}
        onChange={handleChange}
        placeholder="Image URL"
        required
      />
      <button type="submit">Create Meme</button>
    </form>
  );
};

export default MemeForm;
