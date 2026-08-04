import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet.heat';
import 'leaflet/dist/leaflet.css';

// Sub-componente que aplica a camada de calor no mapa
function HeatmapLayer({ dados }) {
  const map = useMap();

  useEffect(() => {
    if (!map || dados.length === 0) return;

    // Converte nossas ocorrências no formato exigido pelo plugin: [lat, lng, intensidade]
    const pontosDeCalor = dados.map(occ => [occ.latitude, occ.longitude, 1]);

    const camada = L.heatLayer(pontosDeCalor, {
      radius: 25, // Tamanho do raio de cada ponto
      blur: 15,   // Nível de desfoque para misturar as cores
      maxZoom: 13,
      gradient: { 0.4: '#004aad', 0.6: '#ffc107', 1.0: '#d9534f' } // Azul -> Amarelo -> Vermelho
    }).addTo(map);

    return () => {
      map.removeLayer(camada); // Limpa a camada ao atualizar
    };
  }, [map, dados]);

  return null;
}

export default function Dashboard() {
  const [ocorrencias, setOcorrencias] = useState([]);
  const navigate = useNavigate();

  const buscarOcorrencias = async () => {
    try {
      const res = await axios.get('/api/corporativo/ocorrencias');
      setOcorrencias(res.data);
    } catch (error) {
      console.error("Erro ao buscar dados corporativos:", error);
    }
  };

  useEffect(() => {
    buscarOcorrencias();
  }, []);

  const atualizarStatus = async (id, novoStatus) => {
    try {
      await axios.put(`/api/corporativo/ocorrencias/${id}/status`, { status: novoStatus });
      buscarOcorrencias();
    } catch (error) {
      alert("Erro ao atualizar o status.");
    }
  };

  const total = ocorrencias.length;
  const abertos = ocorrencias.filter(o => o.status === 'Aberto').length;
  const emAndamento = ocorrencias.filter(o => o.status === 'Em Andamento').length;
  const resolvidos = ocorrencias.filter(o => o.status === 'Resolvido').length;

  const fonteCabecalho = "'Neutra Text', sans-serif";
  const fonteCorpo = "'Kelson Sans', sans-serif";
  const centroSalvador = [-12.9777, -38.5016];

  return (
    <div style={{ padding: '2rem', fontFamily: fonteCorpo, maxWidth: '1200px', margin: '0 auto', backgroundColor: '#f4f7f6', minHeight: '100vh' }}>
      
      {/* Cabeçalho */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 style={{ color: '#004aad', margin: 0, fontFamily: fonteCabecalho, letterSpacing: '1px' }}>
          Painel de Gestão - Salvador
        </h2>
        <button
          onClick={() => navigate('/mapa')}
          style={{ padding: '0.8rem 1.2rem', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold', fontFamily: fonteCorpo }}
        >
          Voltar ao Mapa (Cidadão)
        </button>
      </div>

      {/* Grid de 12 colunas para as Métricas */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>
        <div style={{ gridColumn: 'span 3', background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: '5px solid #6c757d' }}>
          <h4 style={{ margin: 0, color: '#6c757d', fontSize: '0.9rem', textTransform: 'uppercase' }}>Total</h4>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '2rem', fontWeight: 'bold', color: '#343a40' }}>{total}</p>
        </div>
        <div style={{ gridColumn: 'span 3', background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: '5px solid #ffc107' }}>
          <h4 style={{ margin: 0, color: '#6c757d', fontSize: '0.9rem', textTransform: 'uppercase' }}>Abertos</h4>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '2rem', fontWeight: 'bold', color: '#343a40' }}>{abertos}</p>
        </div>
        <div style={{ gridColumn: 'span 3', background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: '5px solid #17a2b8' }}>
          <h4 style={{ margin: 0, color: '#6c757d', fontSize: '0.9rem', textTransform: 'uppercase' }}>Em Andamento</h4>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '2rem', fontWeight: 'bold', color: '#343a40' }}>{emAndamento}</p>
        </div>
        <div style={{ gridColumn: 'span 3', background: 'white', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', borderLeft: '5px solid #28a745' }}>
          <h4 style={{ margin: 0, color: '#6c757d', fontSize: '0.9rem', textTransform: 'uppercase' }}>Resolvidos</h4>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '2rem', fontWeight: 'bold', color: '#343a40' }}>{resolvidos}</p>
        </div>
      </div>

      {/* Mapa de Calor ocupando toda a largura (span 12 no grid mental) */}
      <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', marginBottom: '2rem', overflow: 'hidden', height: '400px' }}>
        <MapContainer center={centroSalvador} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; OpenStreetMap contributors'
          />
          <HeatmapLayer dados={ocorrencias} />
        </MapContainer>
      </div>

      {/* Tabela de Dados */}
      <div style={{ overflowX: 'auto', background: 'white', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: '#343a40', color: 'white' }}>
              <th style={{ padding: '1rem' }}>Protocolo</th>
              <th style={{ padding: '1rem' }}>Data</th>
              <th style={{ padding: '1rem' }}>Tipo</th>
              <th style={{ padding: '1rem' }}>Descrição</th>
              <th style={{ padding: '1rem' }}>Status (Ação)</th>
            </tr>
          </thead>
          <tbody>
            {ocorrencias.map((occ) => (
              <tr key={occ.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                <td style={{ padding: '1rem', fontWeight: 'bold', color: '#495057' }}>{occ.protocolo}</td>
                <td style={{ padding: '1rem', color: '#6c757d' }}>{occ.data_criacao}</td>
                <td style={{ padding: '1rem', fontWeight: 'bold' }}>{occ.tipo}</td>
                <td style={{ padding: '1rem', maxWidth: '250px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{occ.descricao}</td>
                <td style={{ padding: '1rem' }}>
                  <select
                    value={occ.status}
                    onChange={(e) => atualizarStatus(occ.id, e.target.value)}
                    style={{
                      padding: '0.5rem',
                      borderRadius: '4px',
                      border: '1px solid #ced4da',
                      background: occ.status === 'Aberto' ? '#fff3cd' : occ.status === 'Em Andamento' ? '#cce5ff' : '#d4edda',
                      color: '#212529',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      width: '100%',
                      fontFamily: fonteCorpo
                    }}
                  >
                    <option value="Aberto">Aberto</option>
                    <option value="Em Andamento">Em Andamento</option>
                    <option value="Resolvido">Resolvido</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}