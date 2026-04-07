import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import StartScreen from './StartScreen';
import GameScreen from './GameScreen';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<StartScreen />} />
          <Route path="/game" element={<GameScreen />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
