# NeuroSearch への貢献 / Contributing to NeuroSearch

NeuroSearch プロジェクトへの貢献を歓迎します！バグ報告、機能提案、コードの改善、ドキュメントの修正など、どのような形でも構いません。

We welcome contributions to the NeuroSearch project! Whether it's bug reports, feature requests, code improvements, or documentation fixes, your help is appreciated.

## 貢献の種類 / Types of Contributions

貢献は以下のようないくつかの形で行うことができます。

Contribution can take several forms:

* **バグ報告 / Bug Reports:** システムの予期しない動作やエラーを見つけた場合は、Issueトラッカーを通じて報告してください。 / If you encounter any unexpected behavior or errors in the system, please report them through the Issue Tracker.
* **機能提案 / Feature Requests:** 新しい機能や改善案があれば、Issueトラッカーで提案してください。 / If you have ideas for new features or enhancements, please suggest them via the Issue Tracker.
* **プルリクエスト (Pull Request) / Pull Requests:** 自身で修正したバグや実装した機能がある場合は、プルリクエストを送信してください。 / If you have fixed a bug or implemented a feature yourself, please submit a Pull Request.
* **ドキュメント / Documentation:** ドキュメントの誤りや改善点を見つけた場合は、Issueトラッカーで報告するか、プルリクエストを送信してください。 / If you find any errors or areas for improvement in the documentation, please report them via the Issue Tracker or submit a Pull Request.
* **翻訳 / Translations:** ドキュメントやUIの翻訳に協力してください。 / Help us translate the documentation or UI into other languages.

## 貢献を始める前に / Before You Start Contributing

* Issueトラッカーで既存のIssueを確認し、同様の問題や提案がないか確認してください。 / Check the Issue Tracker for existing issues or proposals to avoid duplicates.
* 大きな変更を加える場合は、事前にIssueトラッカーで提案し、議論を行うことを推奨します。 / For significant changes, we recommend discussing your ideas in the Issue Tracker before starting implementation.

## バグ報告の方法 / How to Report a Bug

バグを報告する際は、以下の情報を含めてください。

When reporting a bug, please include the following information:

* **再現手順 / Steps to Reproduce:** どのようにバグを再現できるかの具体的な手順。 / Clear and concise steps to reproduce the bug.
* **期待される動作 / Expected Behavior:** 本来どのような動作をするべきだったか。 / What should have happened?
* **実際の動作 / Actual Behavior:** 実際に何が起こったか。 / What actually happened?
* **環境情報 / Environment Information:** OSの種類、Pythonのバージョン、関連するライブラリのバージョンなど。 / Your operating system, Python version, and relevant library versions.
* **エラーメッセージ / Error Messages:** 発生したエラーメッセージの全文 (もしあれば)。 / The full error message if any.

## 機能提案の方法 / How to Suggest a Feature

新しい機能や改善案を提案する際は、以下の情報を含めてください。

When suggesting a new feature or enhancement, please include the following information:

* **提案内容 / Proposal:** 具体的にどのような機能や改善を提案しますか。 / A clear description of the proposed feature or enhancement.
* **背景 / Background:** その機能や改善が必要となる理由や背景。 / The reasons or context for why this feature or enhancement is needed.
* **期待される効果 / Expected Benefits:** その機能や改善によってどのような効果が期待できますか。 / What advantages or improvements would this bring?
* **代替案 / Alternatives:** もしあれば、他の実現方法や代替案。 / If any, other ways to achieve the same goal.

## プルリクエストの送信方法 / How to Submit a Pull Request

コードを貢献する場合は、以下の手順に従ってください。

If you want to contribute code, please follow these steps:

1.  リポジトリをフォークします。 / Fork the repository.
2.  ローカルリポジトリにクローンします。 / Clone the repository to your local machine:
    ```bash
    git clone [https://github.com/](https://github.com/)<あなたのユーザー名>/NeuroSearch.git
    cd NeuroSearch
    ```
    ```bash
    git clone [https://github.com/](https://github.com/)<your_username>/NeuroSearch.git
    cd NeuroSearch
    ```
3.  変更を行うための新しいブランチを作成します。 / Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature-name
    ```
    または / or
    ```bash
    git checkout -b fix/your-bug-fix-name
    ```
4.  コードを変更します。 / Make your code changes.
5.  変更をコミットします。 / Commit your changes:
    ```bash
    git add .
    git commit -m "feat(search): Implement RRF ranking"
    ```
    または / or
    ```bash
    git commit -m "fix(ui): Fix layout issue"
    ```
    コミットメッセージの形式については、後述の「コミットメッセージの規約 / Commit Message Conventions」を参照してください。 / Please refer to the "Commit Message Conventions" below.
6.  リモートリポジトリにプッシュします。 / Push your changes to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
7.  GitHub上で、あなたのフォークしたリポジトリから NeuroSearch のメインリポジトリに対してプルリクエストを作成します。 / Create a Pull Request from your forked repository to the main NeuroSearch repository on GitHub.

## コーディング規約 / Coding Conventions

* PEP 8 に準拠したPythonコードを記述してください。 / Follow PEP 8 style guidelines for Python code.
* 変更を加える際は、関連するテストも追加または修正してください。 / Add or modify relevant tests when making changes.
* コードは明確で理解しやすいように記述してください。 / Write clear and understandable code.
* 大きな変更を加える場合は、コードの意図や設計についてコメントを記述してください。 / For significant changes, add comments to explain the intent and design of your code.

## コミットメッセージの規約 / Commit Message Conventions

コミットメッセージは以下の形式を推奨します。

We recommend the following commit message format:

&lt;type>(&lt;scope>): &lt;subject>

&lt;body>

&lt;footer>


* `<type>`: コミットの種類 (例: `feat` (新機能), `fix` (バグ修正), `docs` (ドキュメント), `style` (コードスタイル), `refactor` (リファクタリング), `test` (テスト), `chore` (ビルドや補助ツールなど)) / The type of the commit (e.g., `feat` for new feature, `fix` for bug fix, `docs` for documentation, `style` for code style, `refactor` for refactoring, `test` for tests, `chore` for build or tooling).
* `<scope>`: 影響を受ける範囲 (例: `ui`, `search`, `summary`, `faq`) (省略可) / The scope of the commit (e.g., `ui`, `search`, `summary`, `faq`). Optional.
* `<subject>`: コミットの簡単な説明 (50文字程度) / A brief description of the commit (around 50 characters).
* `<body>`: 詳細な説明 (必要に応じて複数行) / A more detailed explanation of the commit. Optional, but useful for complex changes.
* `<footer>`: Issueの参照など (例: `Closes #123`, `Refs #456`) (省略可) / References to issues or other related information (e.g., `Closes #123`, `Refs #456`). Optional.

例 / Example:

feat(search): Implement RRF ranking

Adds Reciprocal Rank Fusion to improve search result diversity.

This change introduces a new ranking function that combines results from multiple search engines using the RRF algorithm.

Closes #78


## テスト / Testing

変更を加えた場合は、必ずテストが正常に動作することを確認してください。必要に応じて、新しいテストを追加してください。

Ensure that your changes pass all existing tests. Add new tests as necessary to cover your changes.

## ドキュメント / Documentation

コードの変更に合わせて、関連するドキュメントも更新してください。

Update any relevant documentation to reflect your changes.

## 行動規範 / Code of Conduct

このプロジェクトへの参加者は、[行動規範](CODE_OF_CONDUCT.md) を守ることが期待されます。

Participants in this project are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

## 連絡先 / Contact

質問や不明な点があれば、Issueトラッカーを通じてお気軽にお問い合わせください。

If you have any questions or need clarification, please feel free to ask via the Issue Tracker.

ご協力ありがとうございます！ / Thank you for your contribution\!
