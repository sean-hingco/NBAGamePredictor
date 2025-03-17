import React, { useState, useEffect } from 'react';
import axios from 'axios';

function HomePage() {
  const [games, setGames] = useState([]);
  const [expandedGame, setExpandedGame] = useState(null);
  const [gameDetails, setGameDetails] = useState({});

  useEffect(() => {
    async function fetchGames() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/todays_games');
        setGames(response.data.games);
      } catch (error) {
        console.error("Error fetching today's games:", error);
      }
    }
    fetchGames();
  }, []);

  const toggleGameDetails = async (gameId) => {
    if (expandedGame === gameId) {
      setExpandedGame(null); // Collapse if already expanded
      return;
    }

    // Fetch game details only if not already loaded
    if (!gameDetails[gameId]) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/game_predictions/${gameId}`);
        setGameDetails((prev) => ({
          ...prev,
          [gameId]: response.data
        }));
      } catch (error) {
        console.error(`Error fetching details for game ${gameId}:`, error);
      }
    }

    setExpandedGame(gameId);
  };

  return (
    <div>
      <h1>Today's NBA Games</h1>
      {games.length === 0 ? <p>Loading games...</p> : (
        <ul>
          {games.map((game) => (
            <li key={game.game_id} style={{ marginBottom: '20px' }}>
              <button onClick={() => toggleGameDetails(game.game_id)}>
                {game.home_team} vs {game.away_team}
              </button>
              
              {expandedGame === game.game_id && gameDetails[game.game_id] && (
                <div style={{ marginTop: '10px', padding: '10px', border: '1px solid #ccc' }}>
                  <h2>Predicted Score: {gameDetails[game.game_id].predicted_home_score} - {gameDetails[game.game_id].predicted_away_score}</h2>
                  <h2>Actual Score: {gameDetails[game.game_id].actual_home_score || "N/A"} - {gameDetails[game.game_id].actual_away_score || "N/A"}</h2>

                  <h3>Player Predictions</h3>
                  <ul>
                    {gameDetails[game.game_id].player_predictions.map((player) => (
                      <li key={player.name}>
                        {player.name}: {player.predicted_points} PTS | {player.predicted_assists} AST | {player.predicted_rebounds} REB
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HomePage;
