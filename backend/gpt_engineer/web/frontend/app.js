function App() {
    const [prompt, setPrompt] = React.useState('');
    const [projectPath, setProjectPath] = React.useState('');
    const [apiKey, setApiKey] = React.useState('');
    const [loading, setLoading] = React.useState(false);
    const [result, setResult] = React.useState(null);
    const [error, setError] = React.useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt,
                    project_path: projectPath,
                    openai_api_key: apiKey,
                }),
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Something went wrong');
            }

            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold mb-8 text-center text-white">GPT Engineer Web UI</h1>
            
            <div className="max-w-2xl mx-auto bg-gray-900 rounded-lg shadow-lg p-6 border border-gray-700">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-300">
                            Project Description
                        </label>
                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            className="mt-1 block w-full rounded-md border-gray-600 bg-gray-800 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                            rows="4"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-300">
                            Project Path
                        </label>
                        <input
                            type="text"
                            value={projectPath}
                            onChange={(e) => setProjectPath(e.target.value)}
                            className="mt-1 block w-full rounded-md border-gray-600 bg-gray-800 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-300">
                            OpenAI API Key (optional)
                        </label>
                        <input
                            type="password"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            className="mt-1 block w-full rounded-md border-gray-600 bg-gray-800 text-white shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
                            loading ? 'opacity-50 cursor-not-allowed' : ''
                        }`}
                    >
                        {loading ? 'Generating...' : 'Generate Code'}
                    </button>
                </form>

                {error && (
                    <div className="mt-4 p-4 bg-red-900 border border-red-700 text-red-100 rounded">
                        {error}
                    </div>
                )}

                {result && (
                    <div className="mt-4">
                        <h2 className="text-lg font-medium text-gray-300">Generated Code:</h2>
                        <pre className="mt-2 p-4 bg-gray-800 text-gray-100 rounded overflow-auto border border-gray-700">
                            {JSON.stringify(result, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));