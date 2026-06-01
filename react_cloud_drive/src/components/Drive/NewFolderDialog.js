import React, { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, Button,
} from '@mui/material';
import client from '../../api/client';

export default function NewFolderDialog({ open, onClose, currentFolder, onCreated }) {
  const [name, setName] = useState('');

  async function handleCreate() {
    if (!name.trim()) return;
    await client.post('/folders/', {
      name: name.trim(),
      parent: currentFolder?.id ?? null,
    });
    setName('');
    onClose();
    onCreated?.();
  }

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="xs">
      <DialogTitle>新增資料夾</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus fullWidth label="資料夾名稱" margin="dense"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>取消</Button>
        <Button variant="contained" onClick={handleCreate} disabled={!name.trim()}>建立</Button>
      </DialogActions>
    </Dialog>
  );
}
