import { useState, useCallback } from 'react';
import { filesApi, gptApi, workspaceApi } from '../api/client';

export function useFilesApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const listFiles = useCallback(async (path: string) => {
        setLoading(true);
        setError(null);
        try {
            return await filesApi.listFiles(path);
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    const readFile = useCallback(async (path: string) => {
        setLoading(true);
        setError(null);
        try {
            return await filesApi.readFile(path);
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    const writeFile = useCallback(async (path: string, content: string | Blob) => {
        setLoading(true);
        setError(null);
        try {
            await filesApi.writeFile(path, content);
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        loading,
        error,
        listFiles,
        readFile,
        writeFile,
        createDirectory: filesApi.createDirectory,
        delete: filesApi.delete,
    };
}

export function useGptApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const generateCode = useCallback(async (prompt: string, workspacePath: string, options?: Record<string, any>) => {
        setLoading(true);
        setError(null);
        try {
            return await gptApi.generateCode({ prompt, workspace_path: workspacePath, options });
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        loading,
        error,
        generateCode,
        getStatus: gptApi.getStatus,
        stopGeneration: gptApi.stopGeneration,
    };
}

export function useWorkspaceApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const getInfo = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            return await workspaceApi.getInfo();
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    const updateConfig = useCallback(async (config: Record<string, any>) => {
        setLoading(true);
        setError(null);
        try {
            await workspaceApi.updateConfig(config);
        } catch (e) {
            setError(e as Error);
            throw e;
        } finally {
            setLoading(false);
        }
    }, []);

    return {
        loading,
        error,
        getInfo,
        updateConfig,
        initialize: workspaceApi.initialize,
    };
}