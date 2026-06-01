import React, { useState } from 'react';
import {
  Card, CardActionArea, CardContent, Typography,
  IconButton, Menu, MenuItem, Box,
} from '@mui/material';
import { Folder, MoreVert, DeleteOutlined } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import client from '../../api/client';

export default function FolderItem({ folder, onDeleted }) {
  const navigate = useNavigate();
  const [anchor, setAnchor] = useState(null);

  async function handleDelete(e) {
    e.stopPropagation();
    setAnchor(null);
    try {
      await client.delete(`/folders/${folder.id}/`);
      onDeleted?.();
    } catch {
      alert('刪除資料夾失敗，請稍後再試。');
    }
  }

  return (
    <Card variant="outlined" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
      <CardActionArea onClick={() => navigate(`/folder/${folder.id}`)} sx={{ flex: 1, p: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Folder sx={{ color: 'warning.main', fontSize: 32 }} />
          <Typography noWrap variant="body1">{folder.name}</Typography>
        </Box>
      </CardActionArea>
      <IconButton size="small" sx={{ mr: 1 }} onClick={(e) => setAnchor(e.currentTarget)}>
        <MoreVert fontSize="small" />
      </IconButton>
      <Menu anchorEl={anchor} open={Boolean(anchor)} onClose={() => setAnchor(null)}>
        <MenuItem onClick={handleDelete} sx={{ color: 'error.main' }}>
          <DeleteOutlined sx={{ mr: 1 }} fontSize="small" /> 刪除
        </MenuItem>
      </Menu>
    </Card>
  );
}
