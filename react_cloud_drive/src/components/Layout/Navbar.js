import React, { useState } from 'react';
import {
  AppBar, Toolbar, Typography, IconButton, Avatar,
  Menu, MenuItem, Box, Tooltip,
} from '@mui/material';
import { CloudQueue, Logout, AccountCircle } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Navbar() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();
  const [anchor, setAnchor] = useState(null);

  async function handleLogout() {
    await logout();
    navigate('/login');
  }

  const initials = currentUser?.displayName
    ? currentUser.displayName.charAt(0).toUpperCase()
    : currentUser?.email?.charAt(0).toUpperCase();

  return (
    <AppBar position="fixed" elevation={1} sx={{ bgcolor: 'background.paper', color: 'text.primary' }}>
      <Toolbar>
        <CloudQueue sx={{ color: 'primary.main', mr: 1 }} />
        <Typography variant="h6" fontWeight={700} sx={{ flexGrow: 1 }}>
          React Cloud Drive
        </Typography>
        <Tooltip title={currentUser?.displayName || currentUser?.email}>
          <IconButton onClick={(e) => setAnchor(e.currentTarget)}>
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main', fontSize: 14 }}>
              {initials}
            </Avatar>
          </IconButton>
        </Tooltip>
        <Menu anchorEl={anchor} open={Boolean(anchor)} onClose={() => setAnchor(null)}>
          <MenuItem disabled>
            <AccountCircle sx={{ mr: 1 }} />
            {currentUser?.email}
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <Logout sx={{ mr: 1 }} />
            登出
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
