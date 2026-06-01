import React from 'react';
import { Breadcrumbs, Link, Typography } from '@mui/material';
import { NavigateNext, Home } from '@mui/icons-material';
import { Link as RouterLink } from 'react-router-dom';
import { ROOT_FOLDER } from '../../hooks/useFolder';

export default function Breadcrumb({ currentFolder }) {
  const path = currentFolder === ROOT_FOLDER ? [] : (currentFolder?.path || []);

  return (
    <Breadcrumbs separator={<NavigateNext fontSize="small" />} sx={{ mb: 2 }}>
      {currentFolder === ROOT_FOLDER ? (
        <Typography color="text.primary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <Home fontSize="small" /> My Drive
        </Typography>
      ) : (
        <Link
          component={RouterLink}
          to="/"
          underline="hover"
          color="inherit"
          sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
        >
          <Home fontSize="small" /> My Drive
        </Link>
      )}
      {path.map((folder) => (
        <Link
          key={folder.id}
          component={RouterLink}
          to={`/folder/${folder.id}`}
          underline="hover"
          color="inherit"
        >
          {folder.name}
        </Link>
      ))}
      {currentFolder !== ROOT_FOLDER && (
        <Typography color="text.primary">{currentFolder?.name}</Typography>
      )}
    </Breadcrumbs>
  );
}
