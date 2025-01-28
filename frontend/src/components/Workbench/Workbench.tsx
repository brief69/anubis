import React, { useState } from 'react';
import { FileExplorer } from '../FileExplorer/FileExplorer';
import { Editor } from '../Editor/Editor';
import { FileInfo } from '../../api/client';
import './Workbench.css';

export const Workbench: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<FileInfo | null>(null);

    const handleFileSelect = (file: FileInfo) => {
        if (!file.is_dir) {
            setSelectedFile(file);
        }
    };

    const getFileLanguage = (fileName: string): string => {
        const extension = fileName.split('.').pop()?.toLowerCase();
        switch (extension) {
            case 'js':
                return 'javascript';
            case 'ts':
                return 'typescript';
            case 'jsx':
                return 'javascript';
            case 'tsx':
                return 'typescript';
            case 'py':
                return 'python';
            case 'json':
                return 'json';
            case 'md':
                return 'markdown';
            case 'css':
                return 'css';
            case 'html':
                return 'html';
            default:
                return 'plaintext';
        }
    };

    return (
        <div className="workbench">
            <div className="sidebar">
                <FileExplorer onFileSelect={handleFileSelect} />
            </div>
            <div className="main-content">
                {selectedFile ? (
                    <Editor
                        filePath={selectedFile.path}
                        language={getFileLanguage(selectedFile.name)}
                    />
                ) : (
                    <div className="welcome-message">
                        <h1>Anubis IDE へようこそ</h1>
                        <p>左のファイルエクスプローラーからファイルを選択してください。</p>
                    </div>
                )}
            </div>
        </div>
    );
};