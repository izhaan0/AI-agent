import React, { useState } from 'react';

function PostGenerator({ userId }) {
  const [post, setPost] = useState('');
  const [scheduledTime, setScheduledTime] = useState('');

  const handleGenerate = async () => {
    const profile = {
      user_id: userId,
      skills: ['mock_skill'],
      experience: ['mock_experience'],
      interests: ['mock_interest'],
    };
    const response = await fetch('http://localhost:8000/generate_post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile),
    });
    const data = await response.json();
    setPost(data.post_content);
  };

  const handleSchedule = async () => {
    await fetch('http://localhost:8000/schedule_post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: post, scheduled_time: scheduledTime, user_id: userId }),
    });
    alert('Post scheduled!');
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Generate LinkedIn Post</h2>
      <button
        onClick={handleGenerate}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg mb-4 hover:bg-blue-700"
      >
        Generate Post
      </button>
      {post && (
        <div>
          <textarea
            value={post}
            readOnly
            className="w-full p-2 mb-4 border rounded"
          />
          <input
            type="datetime-local"
            value={scheduledTime}
            onChange={(e) => setScheduledTime(e.target.value)}
            className="w-full p-2 mb-4 border rounded"
          />
          <button
            onClick={handleSchedule}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Schedule Post
          </button>
        </div>
      )}
    </div>
  );
}

export default PostGenerator;