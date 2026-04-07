import React, { useState, useEffect } from 'react';
import { startGame, makeTurn } from './api';

// Game State Display Component
const GameStateDisplay = ({ state }) => {
  return (
    <div className="game-state">
      <h1>📍 {state.location}</h1>
      <div className="game-stats">
        {/* <p><strong>Day:</strong> {state.day}/{60}</p> */}
        <label><strong>Product Progress:</strong> {state.product_progress}%</label>
        <meter min="0" max="100" low="33" high="66" optimum="80" value={state.product_progress}> 
          product progress: {state.product_progress}%
        </meter>

        <p><strong>Money:</strong> ${state.money}</p>
        <label><strong>Chemistry:</strong> {state.chemistry}%</label>
        <meter min="0" max="100" low="33" high="66" optimum="80" value={state.chemistry}> 
          chemistry: {state.chemistry}%
        </meter>
        <p><strong>Followers:</strong> {state.followers}</p>
        <p><strong>Features:</strong> {state.features.length} ({state.features.join(', ') || 'None yet'})</p>
        <p><strong>Days Left:</strong> {state.days_left}</p>
      </div>
    </div>
  );
};

// Choice Component
const ChoiceComponent = ({ choices, onChoose }) => {
  if (!choices || choices.length === 0) {
    return <div className="choices"><p>No choices available</p></div>;
  }

  return (
    <div className="choices">
      <h3>Choose Your Action:</h3>
      {choices.map((choice, index) => (
        <button 
          key={choice.key || index} 
          onClick={() => onChoose(choice.key)}
          className="choice-btn"
        >
          {choice.label}
        </button>
      ))}
    </div>
  );
};

const formatEffects = (effects) => {
  const labels = {
    money: (v) => `${v >= 0 ? '+' : ''}$${v}`,
    product_progress: (v) => `${v >= 0 ? '+' : ''}${v}% Product Progress`,
    chemistry: (v) => `${v >= 0 ? '+' : ''}${v}% Team Chemistry`,
    followers: (v) => `${v >= 0 ? '+' : ''}${v} Followers`,
    day: (v) => `+${Math.abs(v)} Day${Math.abs(v) !== 1 ? 's' : ''}`,
  };
  return Object.entries(effects).map(([key, val]) => {
    const formatter = labels[key];
    return formatter ? formatter(val) : `${key}: ${val}`;
  });
};

// Event Component
const EventComponent = ({ event }) => {
  if (!event) return null;
  const effectLines = event.effects ? formatEffects(event.effects) : [];
  return (
    <div className="event">
      <h3>⚡ {event.name}</h3>
      <p>{event.description}</p>
      {effectLines.length > 0 && (
        <ul className="event-effects">
          {effectLines.map((line, i) => <li key={i}>{line}</li>)}
        </ul>
      )}
    </div>
  );
};

// Travel Component
const TravelComponent = ({ onTravel }) => {
  return (
    <div className="travel">
      <h3>Travel to Next Location</h3>
      <button onClick={onTravel}>Travel</button>
    </div>
  );
};

// Crypto Event Component
const CryptoEventComponent = ({ cryptoEvent }) => {
  if (!cryptoEvent) return null;
  return (
    <div className="crypto-event">
      <p>{cryptoEvent.message}</p>
    </div>
  );
};

// Main Game Component
const GameScreen = () => {
  const [gameState, setGameState] = useState(null);
  const [currentEvent, setCurrentEvent] = useState(null);
  const [choices, setChoices] = useState([]);
  const [isTraveling, setIsTraveling] = useState(false);
  const [travelEvent, setTravelEvent] = useState(null);
  const [gameOver, setGameOver] = useState(null); // { status: 'win'|'lose', message: '' }
  const [cryptoEvent, setCryptoEvent] = useState(null);

  const getBackgroundImage = (location) => {
    const gradients = {
      "New York, NY":        "linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%)",
      "Philadelphia, PA":   "linear-gradient(135deg, #2d1b33 0%, #4a235a 50%, #6c3483 100%)",
      "Washington, DC":     "linear-gradient(135deg, #1b2631 0%, #1f4e79 50%, #2e86c1 100%)",
      "Raleigh, NC":        "linear-gradient(135deg, #145a32 0%, #1e8449 50%, #27ae60 100%)",
      "Atlanta, GA":        "linear-gradient(135deg, #1a0a00 0%, #7d3c0a 50%, #ca6f1e 100%)",
      "Austin, TX":         "linear-gradient(135deg, #4a0e0e 0%, #922b21 50%, #c0392b 100%)",
      "Denver, CO":         "linear-gradient(135deg, #1c2833 0%, #2e4057 50%, #5d7a9a 100%)",
      "Boulder, CO":        "linear-gradient(135deg, #0d3349 0%, #1a6b8a 50%, #21a0c4 100%)",
      "Salt Lake City, UT": "linear-gradient(135deg, #2c2c2c 0%, #5d4037 50%, #8d6e63 100%)",
      "Palo Alto, CA":      "linear-gradient(135deg, #1a3a1a 0%, #2d6a2d 50%, #52a152 100%)",
      "San Francisco, CA":  "linear-gradient(135deg, #0d0d2b 0%, #1a237e 40%, #f57f17 100%)",
    };
    return gradients[location] || "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)";
  };

  useEffect(() => {
    // Initialize game state when component mounts
    startGame()
      .then(data => {
        setGameState(data.state);
        setChoices(data.choices || []);
      })
      .catch(err => console.error('Error starting game:', err));
  }, []);

  const makeChoice = (choiceKey) => {
    makeTurn(choiceKey)
      .then(data => {
        setGameState(data.state);
        setChoices(data.choices || []);
        setCurrentEvent(data.event);
        setCryptoEvent(data.crypto_event || null);
        if (data.status === 'win' || data.status === 'lose' || data.status === 'game_over') {
          setGameOver({ status: data.status, message: data.message });
        }
      })
      .catch(err => console.error('Error making choice:', err));
  };

  const travel = () => {
    setIsTraveling(true);
    setTravelEvent(null);
    makeTurn('travel')
      .then(data => {
        setTravelEvent(data.event);
        // Show event on loading screen for 3 seconds, then reveal new city
        setTimeout(() => {
          setGameState(data.state);
          setChoices(data.choices || []);
          setCurrentEvent(data.event);
          setIsTraveling(false);
          if (data.status === 'win' || data.status === 'lose' || data.status === 'game_over') {
            setGameOver({ status: data.status, message: data.message });
          }
        }, 3000);
      })
      .catch(err => {
        console.error('Error making choice:', err);
        setIsTraveling(false);
      });
  };

  if (!gameState) {
    return <div>Loading...</div>;
  }

  if (gameOver) {
    return (
      <div className="game" style={{ backgroundImage: getBackgroundImage(gameState.location) }}>
        <div className="travel-loading">
          <h2>{gameOver.status === 'win' ? '🎉 You Won!' : '💀 Game Over'}</h2>
          <p>{gameOver.message}</p>
          <button onClick={() => window.location.reload()}>Play Again</button>
        </div>
      </div>
    );
  }

  if (isTraveling) {
    return (
      <div className="game" style={{ backgroundImage: getBackgroundImage(gameState.location) }}>
        <div className="travel-loading">
          <h2>Traveling...</h2>
          <div className="loading-spinner"></div>
          {travelEvent ? (
            <div className="travel-event">
              <h3>⚡ {travelEvent.name}</h3>
              <p>{travelEvent.description}</p>
            </div>
          ) : (
            <p>Heading to the next city...</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="game" style={{ backgroundImage: getBackgroundImage(gameState.location) }}>
      <GameStateDisplay state={gameState} />
      <EventComponent event={currentEvent} />
      <CryptoEventComponent cryptoEvent={cryptoEvent} />
      <ChoiceComponent choices={choices} onChoose={makeChoice} />
      <TravelComponent onTravel={travel} />
    </div>
  );
};

export default GameScreen;