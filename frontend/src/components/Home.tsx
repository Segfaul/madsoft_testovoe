import React from "react";

import MemeCards from './meme/MemeCards';
import MemeForm from './meme/MemeForm';

const Home: React.FC = () => {
    return (
        <div className="home">
            <MemeForm />
            <MemeCards />
        </div>
    );
}

export default Home;