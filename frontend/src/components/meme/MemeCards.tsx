import React, { useState, useEffect } from 'react';
import { client_public } from '../config/client';
import { Meme, PageParams } from '../config/types';

const MemeCards: React.FC = () => {
  const [memes, setMemes] = useState<Meme[]>([]);
  const [pageParams, setPageParams] = useState<PageParams>({
    limit: 2,
    offset: 0,
  });

  useEffect(() => {
    const fetchMemes = async () => {
      try {
        const response = await client_public.get<Meme[]>('/api/v1/meme', {
          params: pageParams,
        });
        setMemes(response.data);
      } catch (error) {
        console.error('Error fetching memes:', error);
      }
    };

    fetchMemes();
  }, [pageParams]);

  const handleNextPage = () => {
    setPageParams((prevParams) => ({
      ...prevParams,
      offset: prevParams.offset + prevParams.limit,
    }));
  };

  const handlePrevPage = () => {
    setPageParams((prevParams) => ({
      ...prevParams,
      offset: Math.max(0, prevParams.offset - prevParams.limit),
    }));
  };

  return (
    <div>
      <h2>Meme Cards</h2>
      <div>
        {memes.map((meme) => (
          <div key={meme.id} style={{ border: '1px solid #ccc', padding: '10px', margin: '10px', width: '300px' }}>
            <img src={meme.image_url} alt={meme.title} style={{ maxWidth: '100%', height: 'auto' }} />
            <h3>{meme.title}</h3>
            <p>{meme.description}</p>
          </div>
        ))}
      </div>
      <div>
        <button onClick={handlePrevPage} disabled={pageParams.offset === 0}>
          Previous Page
        </button>
        <button onClick={handleNextPage}>
          Next Page
        </button>
      </div>
    </div>
  );
};

export default MemeCards;
