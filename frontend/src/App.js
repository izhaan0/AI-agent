import React, { useState } from 'react';
import Auth from './components/Auth';
import ProfileForm from './components/ProfileForm';
import PostGenerator from './components/PostGenerator';
import './App.css';

function App() {
  const [userId, setUserId] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <h1 className="text-3xl font-bold mb-6">LinkedIn Personal Branding AI Agent</h1>
      {!userId ? (
        <Auth setUserId={setUserId} />
      ) : (
        <div className="w-full max-w-2xl">
          <ProfileForm userId={userId} />
          <PostGenerator userId={userId} />
        </div>
      )}
    </div>
  );
}

export default App;