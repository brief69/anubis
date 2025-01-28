# Anubis

Web対応のモダンなIDE。VoidエディタとGPT Engineerを統合し、AIによるコード生成・編集機能を提供します。

## プロジェクト構成

```
anubis/
├── frontend/     # Voidベースのウェブエディタ
└── backend/      # GPT Engineer統合用バックエンド
```

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