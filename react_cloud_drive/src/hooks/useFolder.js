import { useState, useEffect } from 'react';
import client from '../api/client';

export const ROOT_FOLDER = { name: 'My Drive', id: null, path: [] };

export function useFolder(folderId = null) {
  const [folder, setFolder] = useState(ROOT_FOLDER);
  const [childFolders, setChildFolders] = useState([]);
  const [childFiles, setChildFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (folderId == null) {
      setFolder(ROOT_FOLDER);
    } else {
      client.get(`/folders/${folderId}/`).then((res) => setFolder(res.data));
    }
  }, [folderId]);

  useEffect(() => {
    setLoading(true);
    const parent = folderId ?? 'null';
    Promise.all([
      client.get(`/folders/?parent=${parent}`),
      client.get(`/files/?folder=${parent}`),
    ]).then(([fRes, fileRes]) => {
      setChildFolders(Array.isArray(fRes.data) ? fRes.data : (fRes.data?.results ?? []));
      setChildFiles(Array.isArray(fileRes.data) ? fileRes.data : (fileRes.data?.results ?? []));
    }).catch(() => {
      setChildFolders([]);
      setChildFiles([]);
    }).finally(() => setLoading(false));
  }, [folderId]);

  function refresh() {
    const parent = folderId ?? 'null';
    Promise.all([
      client.get(`/folders/?parent=${parent}`),
      client.get(`/files/?folder=${parent}`),
    ]).then(([fRes, fileRes]) => {
      setChildFolders(Array.isArray(fRes.data) ? fRes.data : (fRes.data?.results ?? []));
      setChildFiles(Array.isArray(fileRes.data) ? fileRes.data : (fileRes.data?.results ?? []));
    });
  }

  return { folder, childFolders, childFiles, loading, refresh };
}
