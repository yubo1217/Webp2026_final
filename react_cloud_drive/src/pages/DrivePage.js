import React, { useState } from 'react';
import { Box, Button, Divider, Typography, Grid } from '@mui/material';
import { CreateNewFolder } from '@mui/icons-material';
import Navbar from '../components/Layout/Navbar';
import Breadcrumb from '../components/Drive/Breadcrumb';
import FolderItem from '../components/Drive/FolderItem';
import FileItem from '../components/Drive/FileItem';
import NewFolderDialog from '../components/Drive/NewFolderDialog';
import UploadButton from '../components/Drive/UploadButton';
import { useFolder } from '../hooks/useFolder';
import { useParams } from 'react-router-dom';

export default function DrivePage() {
  const { folderId } = useParams();
  const { folder, childFolders, childFiles, refresh } = useFolder(folderId ?? null);
  const [dialogOpen, setDialogOpen] = useState(false);

  const isEmpty = childFolders.length === 0 && childFiles.length === 0;

  return (
    <>
      <Navbar />
      <Box sx={{ mt: 8, px: { xs: 2, sm: 4 }, py: 3, maxWidth: 900, mx: 'auto' }}>
        <Breadcrumb currentFolder={folder} />
        <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
          <UploadButton currentFolder={folder} onUploaded={refresh} />
          <Button variant="outlined" startIcon={<CreateNewFolder />} onClick={() => setDialogOpen(true)}>
            新增資料夾
          </Button>
        </Box>

        {childFolders.length > 0 && (
          <>
            <Typography variant="subtitle2" color="text.secondary" mb={1}>資料夾</Typography>
            <Grid container spacing={1} mb={2}>
              {childFolders.map((f) => (
                <Grid item xs={12} sm={6} key={f.id}>
                  <FolderItem folder={f} onDeleted={refresh} />
                </Grid>
              ))}
            </Grid>
            <Divider sx={{ mb: 2 }} />
          </>
        )}

        {childFiles.length > 0 && (
          <>
            <Typography variant="subtitle2" color="text.secondary" mb={1}>檔案</Typography>
            <Grid container spacing={1}>
              {childFiles.map((f) => (
                <Grid item xs={12} sm={6} key={f.id}>
                  <FileItem file={f} onDeleted={refresh} />
                </Grid>
              ))}
            </Grid>
          </>
        )}

        {isEmpty && (
          <Box sx={{ textAlign: 'center', mt: 10, color: 'text.disabled' }}>
            <Typography variant="h6">此資料夾是空的</Typography>
            <Typography variant="body2">上傳檔案或建立資料夾來開始使用</Typography>
          </Box>
        )}
      </Box>

      <NewFolderDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        currentFolder={folder}
        onCreated={refresh}
      />
    </>
  );
}
