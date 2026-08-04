import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Sub-componente para escutar os cliques no mapa
function CapturadorDeClique({ aoClicar }) {
  useMapEvents({
    click(evento) {
      aoClicar(evento.latlng);
    },
  });
  return null;
}

export default function Mapa() {
  const [ocorrencias, setOcorrencias] = useState([]);
  const [modoSelecao, setModoSelecao] = useState(false);
  const [mostrarModal, setMostrarModal] = useState(false);
  const [novaCoordenada, setNovaCoordenada] = useState(null);
  
  // Estados para o formulário
  const [tipo, setTipo] = useState('Buraco na via');
  const [descricao, setDescricao] = useState('');

  // Busca os dados ao carregar
  const buscarDados = async () => {
    try {
      const res = await axios.get('/api/cidadao/ocorrencias');
      setOcorrencias(res.data);
    } catch (error) {
      console.error("Erro ao buscar as ocorrências:", error);
    }
  };

  useEffect(() => {
    buscarDados();
  }, []);

  const lidarComCliqueNoMapa = (latlng) => {
    if (modoSelecao) {
      setNovaCoordenada(latlng);
      setMostrarModal(true);
      setModoSelecao(false); // Desliga o modo de seleção
    }
  };

  const enviarOcorrencia = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/cidadao/registrar', {
        tipo,
        descricao,
        latitude: novaCoordenada.lat,
        longitude: novaCoordenada.lng
      });
      
      // Limpa e fecha o modal
      setMostrarModal(false);
      setDescricao('');
      
      // Atualiza os marcadores na tela
      buscarDados();
      alert("Ocorrência registrada com sucesso na nuvem!");
      
    } catch (error) {
      alert("Erro ao registrar a ocorrência.");
    }
  };

  const centroSalvador = [-12.9777, -38.5016];

  return (
    <div style={{ height: '100vh', width: '100vw', position: 'relative' }}>
      <div style={{ background: '#004aad', color: 'white', padding: '1rem', textAlign: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.2)', position: 'relative', zIndex: 1000 }}>
        <h3 style={{ margin: 0 }}>RepareAqui - Mapa da Cidade</h3>
      </div>

      {/* Aviso flutuante indicando o modo de seleção */}
      {modoSelecao && (
        <div style={{ position: 'absolute', top: '70px', left: '50%', transform: 'translateX(-50%)', background: '#ffc107', color: 'black', padding: '10px 20px', borderRadius: '20px', zIndex: 1000, fontWeight: 'bold', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }}>
          📍 Clique no mapa para marcar o local do problema
        </div>
      )}

      <MapContainer center={centroSalvador} zoom={13} style={{ height: 'calc(100vh - 60px)', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        
        <CapturadorDeClique aoClicar={lidarComCliqueNoMapa} />
        
        {ocorrencias.map((occ) => (
          <Marker key={occ.id} position={[occ.latitude, occ.longitude]}>
            <Popup>
              <div style={{ fontFamily: 'sans-serif' }}>
                <strong style={{ color: '#004aad', fontSize: '1.1rem' }}>{occ.tipo}</strong>
                <p style={{ margin: '0.5rem 0' }}>{occ.descricao}</p>
                <span style={{ fontSize: '0.85rem', color: '#666' }}>
                  <strong>Protocolo:</strong> {occ.protocolo} <br/>
                  <strong>Status:</strong> {occ.status}
                </span>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {/* Botão de Ação Flutuante (FAB) */}
      {!modoSelecao && !mostrarModal && (
        <button 
          onClick={() => setModoSelecao(true)}
          style={{ position: 'absolute', bottom: '30px', right: '30px', zIndex: 1000, background: '#d9534f', color: 'white', border: 'none', borderRadius: '50%', width: '60px', height: '60px', fontSize: '30px', cursor: 'pointer', boxShadow: '0 4px 8px rgba(0,0,0,0.3)', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          +
        </button>
      )}

      {/* Janela Modal do Formulário */}
      {mostrarModal && (
        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.5)', zIndex: 2000, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <div style={{ background: 'white', padding: '20px', borderRadius: '8px', width: '90%', maxWidth: '400px', fontFamily: 'sans-serif' }}>
            <h3 style={{ marginTop: 0, color: '#004aad' }}>Nova Ocorrência</h3>
            <form onSubmit={enviarOcorrencia} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Categoria:</label>
                <select value={tipo} onChange={(e) => setTipo(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
                  <option value="Buraco na via">Buraco na via</option>
                  <option value="Semáforo quebrado">Semáforo quebrado</option>
                  <option value="Iluminação pública">Iluminação pública queimada</option>
                  <option value="Entulho na calçada">Entulho na calçada</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Descrição:</label>
                <textarea 
                  value={descricao} 
                  onChange={(e) => setDescricao(e.target.value)} 
                  required
                  rows="3"
                  placeholder="Detalhes adicionais..."
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', resize: 'none' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                <button type="button" onClick={() => setMostrarModal(false)} style={{ padding: '10px', background: '#ccc', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Cancelar</button>
                <button type="submit" style={{ padding: '10px', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Salvar Problema</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}