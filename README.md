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
│   ├── gpt_engineer/       # GPT Engineerのコア
│   └── pyproject.toml      # バックエンドの依存関係
└── README.md

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