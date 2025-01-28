# Anubis IDE

モダンなウェブベースの統合開発環境

## 開発環境のセットアップ

### フロントエンド

1. 依存関係のインストール
```bash
cd frontend
npm install
```

2. 開発サーバーの起動
```bash
npm run dev
```

3. その他のコマンド
```bash
# プロダクションビルド
npm run build

# ビルドディレクトリのクリーン
npm run clean
```

### バックエンド

1. 依存関係のインストール
```bash
cd backend
poetry install
```

2. 開発サーバーの起動
```bash
poetry run uvicorn src.api.main:app --reload
```

3. テストの実行
```bash
poetry run pytest
```

## テスト

### バックエンドテスト

以下のテストが実装されています：

1. **ファイル操作API**
   - ファイル一覧の取得
   - ファイルの読み書き
   - ディレクトリの作成・削除
   - エラーケースの処理

2. **GPTサービス**
   - タスクの開始と実行
   - 生成プロセスの管理
   - タスクの停止機能
   - ステータス管理

3. **ワークスペース管理**
   - 情報取得
   - 設定の更新
   - 初期化処理

## プロジェクト構造

```
anubis/
├── frontend/                  # フロントエンド（Voidベース）
│   ├── src/                  # ソースコード
│   │   ├── vs/              # VSCode/Voidのコアコード
│   │   ├── browser/         # ブラウザ固有の実装
│   │   └── workbench/       # ワークベンチの実装
│   ├── public/              # 静的ファイル
│   │   ├── manifest.json    # PWAマニフェスト
│   │   ├── service-worker.js # Service Worker
│   │   └── media/          # アイコンなどのメディアファイル
│   └── package.json         # フロントエンドの依存関係
├── backend/                  # バックエンド（GPT Engineer）
│   ├── src/
│   │   └── api/            # RESTful API実装
│   │       ├── models/     # データモデル
│   │       ├── routers/    # APIルーター
│   │       └── services/   # ビジネスロジック
│   ├── tests/              # テストコード
│   │   └── api/           # APIテスト
│   ├── gpt_engineer/       # GPT Engineerのコア
│   └── pyproject.toml      # バックエンドの依存関係
└── README.md

## API エンドポイント

### ファイル操作
- `GET /api/files/list/{path}` - ファイル一覧の取得
- `GET /api/files/read/{path}` - ファイルの読み取り
- `POST /api/files/write/{path}` - ファイルの書き込み
- `POST /api/files/create/directory/{path}` - ディレクトリの作成
- `DELETE /api/files/delete/{path}` - ファイル/ディレクトリの削除

### GPT Engineer
- `POST /api/gpt/generate` - コード生成の開始
- `GET /api/gpt/status/{task_id}` - 生成タスクのステータス確認
- `POST /api/gpt/stop/{task_id}` - 生成タスクの停止

### ワークスペース
- `GET /api/workspace/info` - ワークスペース情報の取得
- `POST /api/workspace/config` - 設定の更新
- `POST /api/workspace/init` - ワークスペースの初期化

## 技術スタック

### フロントエンド
- TypeScript/JavaScript
- Monaco Editor
- PWA対応
- File System Access API
- Service Worker

### バックエンド
- Python 3.10+
- FastAPI
- GPT Engineer

## ビルドシステム
- Gulp 5.0
- TypeScriptコンパイラ
- PostCSS（Autoprefixer, cssnano）
- ソースマップ生成
- 開発サーバー（BrowserSync）

## 開発環境のセットアップ

### フロントエンド
```bash
cd frontend
npm install
npm run watch
```

### バックエンド
```bash
cd backend
poetry install
poetry shell
python -m gpt_engineer.main
```

## 開発ステータス
現在フェーズ1の開発中：
- [ ] Voidのウェブブラウザ対応
- [ ] File System Access APIの統合
- [ ] 基本的なエディタ機能の動作確認

## ライセンス
このプロジェクトは、フロントエンド（Void）とバックエンド（GPT Engineer）それぞれのライセンスに従います。 