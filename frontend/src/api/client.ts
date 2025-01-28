/**
 * Anubis IDE APIクライアント
 */

const API_BASE_URL = 'http://localhost:8000/api';

export interface FileInfo {
    name: string;
    path: string;
    is_dir: boolean;
    size?: number;
    modified: number;
}

export interface WorkspaceInfo {
    path: string;
    name: string;
    config: Record<string, any>;
}

export interface CodeGenerationRequest {
    prompt: string;
    workspace_path: string;
    options?: Record<string, any>;
}

export interface CodeGenerationResponse {
    task_id: string;
    status: string;
    result?: Record<string, any>;
    error?: string;
}

/**
 * ファイル操作API
 */
export const filesApi = {
    async listFiles(path: string): Promise<FileInfo[]> {
        const response = await fetch(`${API_BASE_URL}/files/list/${path}`);
        if (!response.ok) throw new Error('Failed to list files');
        return response.json();
    },

    async readFile(path: string): Promise<string> {
        const response = await fetch(`${API_BASE_URL}/files/read/${path}`);
        if (!response.ok) throw new Error('Failed to read file');
        return response.text();
    },

    async writeFile(path: string, content: string | Blob): Promise<void> {
        const formData = new FormData();
        formData.append('file', content);

        const response = await fetch(`${API_BASE_URL}/files/write/${path}`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Failed to write file');
    },

    async createDirectory(path: string): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/files/create/directory/${path}`, {
            method: 'POST',
        });

        if (!response.ok) throw new Error('Failed to create directory');
    },

    async delete(path: string): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/files/delete/${path}`, {
            method: 'DELETE',
        });

        if (!response.ok) throw new Error('Failed to delete path');
    },
};

/**
 * GPT Engineer API
 */
export const gptApi = {
    async generateCode(request: CodeGenerationRequest): Promise<CodeGenerationResponse> {
        const response = await fetch(`${API_BASE_URL}/gpt/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) throw new Error('Failed to start code generation');
        return response.json();
    },

    async getStatus(taskId: string): Promise<CodeGenerationResponse> {
        const response = await fetch(`${API_BASE_URL}/gpt/status/${taskId}`);
        if (!response.ok) throw new Error('Failed to get generation status');
        return response.json();
    },

    async stopGeneration(taskId: string): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/gpt/stop/${taskId}`, {
            method: 'POST',
        });

        if (!response.ok) throw new Error('Failed to stop generation');
    },
};

/**
 * ワークスペースAPI
 */
export const workspaceApi = {
    async getInfo(): Promise<WorkspaceInfo> {
        const response = await fetch(`${API_BASE_URL}/workspace/info`);
        if (!response.ok) throw new Error('Failed to get workspace info');
        return response.json();
    },

    async updateConfig(config: Record<string, any>): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/workspace/config`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config),
        });

        if (!response.ok) throw new Error('Failed to update workspace config');
    },

    async initialize(): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/workspace/init`, {
            method: 'POST',
        });

        if (!response.ok) throw new Error('Failed to initialize workspace');
    },
};