import React, { useRef, useState } from 'react';
import { Button, Box, Typography, CircularProgress, Snackbar, Alert } from '@mui/material';
import { UploadFile } from '@mui/icons-material';
import client from '../../api/client';

export default function UploadButton({ currentFolder, onUploaded }) {
  const fileInput = useRef();
  const [uploading, setUploading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  function handleFileChange(e) {
    const files = Array.from(e.target.files);
    e.target.value = '';
    uploadFiles(files);
  }

  async function uploadFiles(files) {
    setUploading(true);
    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);
      if (currentFolder?.id) formData.append('folder', currentFolder.id);
      try {
        await client.post('/files/', formData);
        setSnackbar({ open: true, message: `上傳完成：${file.name}`, severity: 'success' });
      } catch {
        setSnackbar({ open: true, message: `上傳失敗：${file.name}`, severity: 'error' });
      }
    }
    setUploading(false);
    onUploaded?.();
  }

  return (
    <>
      <input ref={fileInput} type="file" multiple hidden onChange={handleFileChange} />
      <Button
        variant="contained"
        startIcon={uploading ? <CircularProgress size={18} color="inherit" /> : <UploadFile />}
        onClick={() => fileInput.current.click()}
        disabled={uploading}
      >
        {uploading ? '上傳中...' : '上傳檔案'}
      </Button>

      <Snackbar
        open={snackbar.open} autoHideDuration={3000}
        onClose={() => setSnackbar((s) => ({ ...s, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar((s) => ({ ...s, open: false }))}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
}
