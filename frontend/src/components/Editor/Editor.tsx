import React, { useEffect, useRef, useState } from 'react';
import * as monaco from 'monaco-editor';
import { useFilesApi } from '../../hooks/useApi';
import './Editor.css';

interface EditorProps {
    filePath: string;
    language?: string;
    onChange?: (content: string) => void;
}

export const Editor: React.FC<EditorProps> = ({
    filePath,
    language,
    onChange,
}) => {
    const editorRef = useRef<HTMLDivElement>(null);
    const [editor, setEditor] = useState<monaco.editor.IStandaloneCodeEditor | null>(null);
    const { loading, error, readFile, writeFile } = useFilesApi();
    const [content, setContent] = useState('');

    useEffect(() => {
        if (editorRef.current && !editor) {
            const newEditor = monaco.editor.create(editorRef.current, {
                value: '',
                language: language || 'plaintext',
                theme: 'vs-dark',
                automaticLayout: true,
                minimap: {
                    enabled: true,
                },
                scrollBeyondLastLine: false,
                fontSize: 14,
                lineNumbers: 'on',
                renderWhitespace: 'selection',
                tabSize: 4,
                insertSpaces: true,
            });

            newEditor.onDidChangeModelContent(() => {
                const newContent = newEditor.getValue();
                setContent(newContent);
                onChange?.(newContent);
            });

            setEditor(newEditor);

            return () => {
                newEditor.dispose();
            };
        }
    }, [editorRef.current]);

    useEffect(() => {
        if (editor && filePath) {
            loadFile();
        }
    }, [filePath, editor]);

    const loadFile = async () => {
        try {
            const fileContent = await readFile(filePath);
            setContent(fileContent);
            editor?.setValue(fileContent);
        } catch (e) {
            console.error('Failed to load file:', e);
        }
    };

    const saveFile = async () => {
        if (!content) return;
        try {
            await writeFile(filePath, content);
            console.log('File saved successfully');
        } catch (e) {
            console.error('Failed to save file:', e);
        }
    };

    useEffect(() => {
        const handleSave = (e: KeyboardEvent) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 's') {
                e.preventDefault();
                saveFile();
            }
        };

        window.addEventListener('keydown', handleSave);
        return () => window.removeEventListener('keydown', handleSave);
    }, [content]);

    if (loading) {
        return <div className="editor-loading">読み込み中...</div>;
    }

    if (error) {
        return <div className="editor-error">エラーが発生しました: {error.message}</div>;
    }

    return (
        <div className="editor-container">
            <div className="editor" ref={editorRef} />
        </div>
    );
};