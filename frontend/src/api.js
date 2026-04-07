// API client for Silicon Valley Trail backend

const API_BASE_URL = 'http://localhost:5000/api';

export const startGame = async () => {
  const response = await fetch(`${API_BASE_URL}/start`);
  if (!response.ok) {
    throw new Error('Failed to start game');
  }
  return response.json();
};

export const makeTurn = async (choice) => {
  const response = await fetch(`${API_BASE_URL}/turn`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ choice }),
  });
  if (!response.ok) {
    throw new Error('Failed to make turn');
  }
  const data = await response.json();
  console.log('[makeTurn]', data);
  return data;
};

export const getIntro = async () => {
  const response = await fetch(`${API_BASE_URL}/intro`);
  if (!response.ok) {
    throw new Error('Failed to load intro');
  }
  return response.json();
};