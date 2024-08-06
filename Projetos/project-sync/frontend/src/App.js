import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [vpnEnabled, setVpnEnabled] = useState(false);
  const [idCondominio, setIdCondominio] = useState('');
  const [idConsulta, setIdConsulta] = useState('');
  const [results, setResults] = useState([]);
  const [showIdConsulta, setShowIdConsulta] = useState(false);

  const handleVpnToggle = () => {
    setVpnEnabled(!vpnEnabled);
  };

  const handleConsulta = async () => {
    if (!vpnEnabled) {
      alert('Por favor, habilite a VPN antes de prosseguir.');
      return;
    }
    const data = { id_condominio: idCondominio };
    if (idConsulta) data.id_consulta = idConsulta;

    try {
      const response = await axios.post('http://localhost:5000/consulta', data);
      setResults(response.data);
      setShowIdConsulta(true);
    } catch (error) {
      console.error('Erro ao consultar:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Consulta de Log de Sincronização</h1>
        <label>
          <input type="checkbox" checked={vpnEnabled} onChange={handleVpnToggle} />
          Habilitar VPN
        </label>
        <br />
        <input
          type="text"
          placeholder="ID do Condomínio"
          value={idCondominio}
          onChange={e => setIdCondominio(e.target.value)}
        />
        <br />
        {showIdConsulta && (
          <input
            type="text"
            placeholder="ID Consulta"
            value={idConsulta}
            onChange={e => setIdConsulta(e.target.value)}
          />
        )}
        <br />
        <button onClick={handleConsulta}>Consultar</button>
        <br />
        <div>
          {results.map(result => (
            <div key={result.id}>
              {JSON.stringify(result)}
            </div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
