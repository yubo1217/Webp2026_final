import React, { useState } from 'react';
import {
  Container, Box, TextField, Button, Typography,
  Alert, Paper, Link, CircularProgress,
} from '@mui/material';
import { CloudQueue } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link as RouterLink } from 'react-router-dom';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', displayName: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (form.password !== form.confirm) return setError('兩次密碼輸入不一致。');
    if (form.password.length < 6) return setError('密碼至少需要 6 個字元。');
    try {
      setError('');
      setLoading(true);
      await register(form.username, form.email, form.password, form.displayName);
      navigate('/');
    } catch (err) {
      const msg = err.data;
      if (msg?.username) setError('此帳號名稱已被使用。');
      else setError('註冊失敗，請確認資料是否正確。');
    } finally {
      setLoading(false);
    }
  }

  const field = (label, key, type = 'text') => (
    <TextField
      label={label} type={type} fullWidth required margin="normal"
      value={form[key]}
      onChange={(e) => setForm({ ...form, [key]: e.target.value })}
    />
  );

  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 10, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <CloudQueue sx={{ fontSize: 56, color: 'primary.main', mb: 1 }} />
        <Typography variant="h5" fontWeight={700} gutterBottom>React Cloud Drive</Typography>
        <Paper elevation={3} sx={{ p: 4, width: '100%', mt: 2 }}>
          <Typography variant="h6" mb={2}>建立帳號</Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            {field('帳號', 'username')}
            {field('顯示名稱', 'displayName')}
            {field('電子郵件', 'email', 'email')}
            {field('密碼', 'password', 'password')}
            {field('確認密碼', 'confirm', 'password')}
            <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }} disabled={loading}>
              {loading ? <CircularProgress size={24} /> : '註冊'}
            </Button>
          </Box>
          <Typography variant="body2" mt={2} textAlign="center">
            已有帳號？ <Link component={RouterLink} to="/login">立即登入</Link>
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}
