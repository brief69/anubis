import React, { useEffect, useState } from 'react';
import { FileInfo } from '../../api/client';
import { useFilesApi } from '../../hooks/useApi';
import './FileExplorer.css';

interface FileExplorerProps {
    initialPath?: string;
    onFileSelect?: (file: FileInfo) => void;
}

export const FileExplorer: React.FC<FileExplorerProps> = ({
    initialPath = '.',
    onFileSelect,
}) => {
    const [currentPath, setCurrentPath] = useState(initialPath);
    const [files, setFiles] = useState<FileInfo[]>([]);
    const { loading, error, listFiles } = useFilesApi();

    useEffect(() => {
        loadFiles(currentPath);
    }, [currentPath]);

    const loadFiles = async (path: string) => {
        try {
            const fileList = await listFiles(path);
            setFiles(fileList.sort((a, b) => {
                // ディレクトリを先に表示
                if (a.is_dir && !b.is_dir) return -1;
                if (!a.is_dir && b.is_dir) return 1;
                // 名前でソート
                return a.name.localeCompare(b.name);
            }));
        } catch (e) {
            console.error('Failed to load files:', e);
        }
    };

    const handleFileClick = (file: FileInfo) => {
        if (file.is_dir) {
            setCurrentPath(file.path);
        } else if (onFileSelect) {
            onFileSelect(file);
        }
    };

    const handleBackClick = () => {
        const parentPath = currentPath.split('/').slice(0, -1).join('/') || '.';
        setCurrentPath(parentPath);
    };

    if (loading) {
        return <div className="file-explorer-loading">読み込み中...</div>;
    }

    if (error) {
        return <div className="file-explorer-error">エラーが発生しました: {error.message}</div>;
    }

    return (
        <div className="file-explorer">
            <div className="file-explorer-header">
                <button
                    onClick={handleBackClick}
                    disabled={currentPath === '.'}
                    className="back-button"
                >
                    ←
                </button>
                <span className="current-path">{currentPath}</span>
            </div>
            <div className="file-list">
                {files.map((file) => (
                    <div
                        key={file.path}
                        className={`file-item ${file.is_dir ? 'directory' : 'file'}`}
                        onClick={() => handleFileClick(file)}
                    >
                        <span className="file-icon">
                            {file.is_dir ? '📁' : '📄'}
                        </span>
                        <span className="file-name">{file.name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};