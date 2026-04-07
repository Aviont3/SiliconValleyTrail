import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getIntro } from './api';

const StartScreen = () => {
  const navigate = useNavigate();
  const [intro, setIntro] = useState(null);

  useEffect(() => {
    getIntro()
      .then(data => setIntro(data))
      .catch(err => console.error('Failed to load intro:', err));
  }, []);

  const handleStart = () => {
    navigate('/game');
  };

  return (
    <div className="start-screen">
      <h1>Silicon Valley Trail</h1>

      {intro ? (
        <>
          <section className="intro-welcome">
            <p>{intro.welcome.description}</p>
          </section>

          <section className="intro-team">
            <h2>{intro.team.title}</h2>
            <ul>
              {intro.team.members.map((m, i) => (
                <li key={i}><strong>{m.name}</strong> — {m.role}</li>
              ))}
            </ul>
          </section>

          <section className="intro-instructions">
            <h2>{intro.instructions.title}</h2>
            <p>{intro.instructions.description}</p>
          </section>
        </>
      ) : (
        <p>Loading...</p>
      )}

      <button onClick={handleStart}>Start Game</button>
    </div>
  );
};

export default StartScreen;