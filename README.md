# NeuroSearch
# マルチAI＆検索ハイブリッドシステム (オープンソース公開版)

このプロジェクトは、Google、Bing、X (Twitter) の検索結果と、FAQ応答を高性能なAIモデルで統合し、より多様で情報源が明確な検索体験を提供するシステムです。

## 概要

ユーザーが入力したクエリに基づいて、複数の検索エンジンから情報を収集し、AIモデル（要約、ランキング、FAQ応答）を用いて処理・統合します。Reciprocal Rank Fusion (RRF) を用いたランキングにより、多様な情報源からの結果が上位に表示されるように工夫されています。

## ライセンス

このソフトウェアは、[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ja) の下で公開されています。

**あなたは以下の条件に従う限り、自由に：**

* **共有:** 本著作物をあらゆる媒体または形式で複製および再配布できます。
* **翻案:** 本著作物をリミックス、変形、および加工できます。

**ただし、以下の条件に従う必要があります：**

* **表示:** あなたは適切なクレジットを表示し、ライセンスへのリンクを提供し、変更があった場合はその旨を示さなければなりません。あなたはこれらを合理的な方法で行うことができますが、著作者があなたまたはあなたの利用を推奨しているような方法で行ってはなりません。
* **非営利:** あなたは営利目的で本著作物を利用してはなりません。
* **継承:** あなたが本著作物をリミックス、変形、または加工した場合、あなたはあなたの派生著作物を元のライセンス（CC BY-NC-SA 4.0）と同じ条件の下で頒布しなければなりません。

## 必要な環境

* Python 3.x
* 必要なPythonライブラリ (後述の `requirements.txt` を参照)
* 各検索エンジンのAPIキー (各自で取得する必要があります)

## APIキーの準備

本システムを利用するには、以下のAPIキーを各自で取得し、`.env` ファイルに設定する必要があります。

1.  **Google Custom Search APIキーとCSE ID:**
    * [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成または選択します。
    * Custom Search API を有効にします。
    * APIキーを作成します。
    * [Google Custom Search Engine](https://cse.google.com/cse/all) で新しい検索エンジンを作成し、CSE ID を取得します。
    * 取得した APIキーと CSE ID を `.env` ファイルに `GOOGLE_API_KEY` および `GOOGLE_CSE_ID` として記述します。

2.  **Bing Search APIキー:**
    * [Azure Portal](https://portal.azure.com/) で Cognitive Services の Bing Search API を検索し、リソースを作成します。
    * 作成したリソースのキーを取得します。
    * 取得した APIキーを `.env` ファイルに `BING_API_KEY` として記述します。

3.  **X (Twitter) APIキー:**
    * [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) でアカウントを作成し、プロジェクトとアプリを作成します。
    * APIキー、APIシークレットキー、ベアラートークンなどを取得します。
    * 取得したベアラートークンを `.env` ファイルに `X_API_KEY` として記述します。

## インストールと実行方法

1.  リポジトリをクローンします。
2.  作業ディレクトリに移動します。
3.  必要なライブラリをインストールします。
    ```bash
    pip install -r requirements.txt
    ```
4.  上記の手順に従って取得したAPIキーを `.env` ファイルに記述します。
5.  Gradio アプリケーションを実行します。
    ```bash
    python app.py
    ```
6.  表示されたURLをブラウザで開きます。

## 貢献方法

バグ報告、機能提案、プルリクエストなど、非営利目的での貢献を歓迎します。貢献に関するガイドラインは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 免責事項

本ソフトウェアは現状有姿で提供され、いかなる保証もありません。作者は、本ソフトウェアの使用によって生じたいかなる損害についても責任を負いません。特に、APIの利用料金については、利用者自身の責任となります。

# Multi-AI & Search Hybrid System (Open Source Edition)

This project integrates search results from Google, Bing, and X (Twitter) with responses from high-performance AI models to provide a more diverse search experience with clear information sources.

## Overview

Based on user input queries, the system collects information from multiple search engines and processes/integrates it using AI models (summarization, ranking, FAQ answering). Ranking using Reciprocal Rank Fusion (RRF) is employed to prioritize results from diverse sources.

## License

This software is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**

* **Share:** copy and redistribute the material in any medium or format.
* **Adapt:** remix, transform, and build upon the material.

**Under the following terms:**

* **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
* **NonCommercial:** You may not use the material for commercial purposes.
* **ShareAlike:** If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original (CC BY-NC-SA 4.0).

## Prerequisites

* Python 3.x
* Required Python libraries (see `requirements.txt` below)
* API keys for each search engine (you need to obtain these yourself)

## Preparing API Keys

To use this system, you need to obtain the following API keys and set them in the `.env` file:

1.  **Google Custom Search API Key and CSE ID:**
    * Create or select a project in the [Google Cloud Console](https://console.cloud.google.com/).
    * Enable the Custom Search API.
    * Create an API key.
    * Create a new search engine at [Google Custom Search Engine](https://cse.google.com/cse/all) and obtain the CSE ID.
    * Enter the obtained API key and CSE ID in the `.env` file as `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`.

2.  **Bing Search API Key:**
    * Search for Bing Search API under Cognitive Services in the [Azure Portal](https://portal.azure.com/) and create a resource.
    * Obtain the key for the created resource.
    * Enter the obtained API key in the `.env` file as `BING_API_KEY`.

3.  **X (Twitter) API Key:**
    * Create an account and a project/app at the [X Developer Portal](https://developer.twitter.com/en/portal/dashboard).
    * Obtain the API key, API secret key, bearer token, etc.
    * Enter the obtained bearer token in the `.env` file as `X_API_KEY`.

## Installation and Usage

1.  Clone the repository.
2.  Navigate to the working directory.
3.  Install the required libraries.
    ```bash
    pip install -r requirements.txt
    ```
4.  Enter the API keys obtained following the steps above into the `.env` file.
5.  Run the Gradio application.
    ```bash
    python app.py
    ```
6.  Open the displayed URL in your browser.

## Contributing

Non-commercial contributions in any form, such as bug reports, feature suggestions, and pull requests, are welcome. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Disclaimer

This software is provided "as is" without any warranty. The author is not responsible for any damages resulting from the use of this software. In particular, the user is solely responsible for any fees associated with the use of the APIs.
