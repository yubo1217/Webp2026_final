import React, { useState } from 'react';
import {
  Card, CardContent, Typography, IconButton, Menu, MenuItem,
  Box, Tooltip,
} from '@mui/material';
import {
  InsertDriveFile, MoreVert, Download, DeleteOutlined,
  Image, PictureAsPdf, VideoFile, AudioFile,
} from '@mui/icons-material';
import client from '../../api/client';

function fileIcon(type) {
  if (type?.startsWith('image/')) return <Image sx={{ color: 'success.main', fontSize: 32 }} />;
  if (type === 'application/pdf') return <PictureAsPdf sx={{ color: 'error.main', fontSize: 32 }} />;
  if (type?.startsWith('video/')) return <VideoFile sx={{ color: 'info.main', fontSize: 32 }} />;
  if (type?.startsWith('audio/')) return <AudioFile sx={{ color: 'secondary.main', fontSize: 32 }} />;
  return <InsertDriveFile sx={{ color: 'text.secondary', fontSize: 32 }} />;
}

function formatBytes(bytes) {
  if (!bytes) return '';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export default function FileItem({ file, onDeleted }) {
  const [anchor, setAnchor] = useState(null);

  async function handleDelete() {
    setAnchor(null);
    try {
      await client.delete(`/files/${file.id}/`);
      onDeleted?.();
    } catch {
      alert('刪除檔案失敗，請稍後再試。');
    }
  }

  return (
    <Card variant="outlined" sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
      <CardContent sx={{ flex: 1, py: 1, '&:last-child': { pb: 1 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {fileIcon(file.mime_type)}
          <Box sx={{ minWidth: 0 }}>
            <Typography noWrap variant="body1">{file.name}</Typography>
            <Typography variant="caption" color="text.secondary">{formatBytes(file.size)}</Typography>
          </Box>
        </Box>
      </CardContent>
      <Tooltip title="下載">
        <IconButton size="small" component="a" href={file.url} target="_blank" rel="noreferrer" download>
          <Download fontSize="small" />
        </IconButton>
      </Tooltip>
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
