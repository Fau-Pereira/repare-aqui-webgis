import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Login() {
  const [email, setEmail] = useState('');
  const [codigo, setCodigo] = useState('');
  const [etapa, setEtapa] = useState(1);
  const [mensagem, setMensagem] = useState('');
  const navigate = useNavigate();

  const pedirToken = async (e) => {
    e.preventDefault();
    setMensagem('Solicitando...');
    try {
      // Graças ao proxy, não precisamos digitar http://localhost:5000
      await axios.post('/api/auth/solicitar-token', { email });
      setEtapa(2);
      setMensagem('Código gerado! Verifique a aba do terminal do backend.');
    } catch (error) {
      setMensagem('Erro ao solicitar acesso. Verifique se o Flask está rodando.');
    }
  };

  const confirmarAcesso = async (e) => {
    e.preventDefault();
    setMensagem('Validando...');
    try {
      const res = await axios.post('/api/auth/validar-token', { email, codigo });
      // Salva os dados do usuário de forma simples no navegador
      localStorage.setItem('usuario', JSON.stringify(res.data.usuario));
      // Redireciona para o mapa
      navigate('/mapa');
    } catch (error) {
      setMensagem('Código inválido ou expirado.');
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '400px', margin: '10vh auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h2 style={{ color: '#004aad' }}>Acesso Cidadão</h2>
      <p style={{ color: '#d9534f', minHeight: '20px' }}>{mensagem}</p>

      {etapa === 1 && (
        <form onSubmit={pedirToken} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <label style={{ textAlign: 'left', fontWeight: 'bold' }}>Seu E-mail (Simulação Gov.br):</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="cidadao@salvador.ba.gov.br"
            style={{ padding: '0.8rem', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button type="submit" style={{ padding: '0.8rem', background: '#004aad', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
            Avançar
          </button>
        </form>
      )}

      {etapa === 2 && (
        <form onSubmit={confirmarAcesso} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <label style={{ textAlign: 'left', fontWeight: 'bold' }}>Código de 6 dígitos:</label>
          <input
            type="text"
            maxLength="6"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
            required
            placeholder="000000"
            style={{ padding: '0.8rem', fontSize: '1.5rem', letterSpacing: '0.5rem', textAlign: 'center', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button type="submit" style={{ padding: '0.8rem', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
            Confirmar Acesso
          </button>
        </form>
      )}
    </div>
  );
}