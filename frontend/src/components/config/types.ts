export interface Meme {
  id: number;
  title: string;
  description: string;
  image_url: string;
}
  
export interface MemeForm {
  title: string;
  description: string | null;
  image_url: string;
}

export interface PageParams {
  limit: number;
  offset: number;
}

export interface MemeURLsResponse {
  urls: string[];
}

export interface UploadMemeResponse {
  filename: string;
  url: string;
}