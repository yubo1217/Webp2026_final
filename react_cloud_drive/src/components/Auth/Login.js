import React, { useState } from 'react';
import {
  Container, Box, TextField, Button, Typography,
  Alert, Paper, Link, CircularProgress,
} from '@mui/material';
import { CloudQueue } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link as RouterLink } from 'react-router-dom';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      setError('');
      setLoading(true);
      await login(form.username, form.password);
      navigate('/');
    } catch {
      setError('登入失敗，請確認帳號密碼是否正確。');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 10, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <CloudQueue sx={{ fontSize: 56, color: 'primary.main', mb: 1 }} />
        <Typography variant="h5" fontWeight={700} gutterBottom>React Cloud Drive</Typography>
        <Paper elevation={3} sx={{ p: 4, width: '100%', mt: 2 }}>
          <Typography variant="h6" mb={2}>登入</Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              label="帳號" fullWidth required margin="normal"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
            <TextField
              label="密碼" type="password" fullWidth required margin="normal"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
            <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }} disabled={loading}>
              {loading ? <CircularProgress size={24} /> : '登入'}
            </Button>
          </Box>
          <Typography variant="body2" mt={2} textAlign="center">
            還沒有帳號？ <Link component={RouterLink} to="/register">立即註冊</Link>
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}
