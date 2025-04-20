import gradio as gr
import aiohttp
import asyncio
import spacy
import os
import torch
import concurrent.futures
import multiprocessing
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForSequenceClassification
from langdetect import detect
from dotenv import load_dotenv
from cachetools import TTLCache
import logging
import numpy as np

# ロギング設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 環境変数の読み込み
load_dotenv()

# 環境変数の取得 (APIキーは各自で用意し、.envファイルに設定することを前提)
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
BING_API_KEY = os.getenv("BING_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")  # X APIキー

# デフォルト設定
DEFAULT_SEARCH_ENGINES = ["google", "bing", "x"]
DEFAULT_SUMMARY_MODEL = "facebook/bart-large-cnn"
DEFAULT_RANKER_MODEL = "cross-encoder/ms-marco-large-v1"
DEFAULT_FAQ_MODEL = "google/flan-t5-large" # より知識に基づいた回答を期待

# キャッシュ設定（10分間有効、最大100エントリ）
cache = TTLCache(maxsize=100, ttl=600)

# モデルの初期化用辞書
nlp_models = {}
summarizer_models = {}
ranker_models = {}
faq_models = {}

# モデルのロード関数 (初回アクセス時にロードし、GPUが利用可能であればGPUを使用)
def load_model(model_name, model_dict, model_class, device=0 if torch.cuda.is_available() else -1, **kwargs):
    if model_name not in model_dict:
        try:
            model_dict[model_name] = model_class.from_pretrained(model_name, **kwargs).to(device)
            logging.info(f"Loaded model: {model_name} on device {device}")
        except Exception as e:
            logging.error(f"Failed to load model {model_name}: {e}")
            model_dict[model_name] = None
    return model_dict[model_name]

# トークナイザーのロード関数 (初回アクセス時にロード)
def load_tokenizer(tokenizer_name, tokenizer_dict):
    if tokenizer_name not in tokenizer_dict:
        try:
            tokenizer_dict[tokenizer_name] = AutoTokenizer.from_pretrained(tokenizer_name)
            logging.info(f"Loaded tokenizer: {tokenizer_name}")
        except Exception as e:
            logging.error(f"Failed to load tokenizer {tokenizer_name}: {e}")
            tokenizer_dict[tokenizer_name] = None
    return tokenizer_dict[tokenizer_name]

# NLPモデルの読み込み (言語ごとにキャッシュ)
def load_nlp_model(lang):
    if lang not in nlp_models:
        model_name = "ja_core_news_sm" if lang == "ja" else "en_core_web_sm"
        try:
            nlp_models[lang] = spacy.load(model_name)
            logging.info(f"Loaded NLP model for {lang}: {model_name}")
        except Exception as e:
            logging.error(f"Failed to load NLP model for {lang}: {e}")
            from spacy.cli import download
            try:
                download(model_name)
                nlp_models[lang] = spacy.load(model_name)
                logging.info(f"Downloaded and loaded NLP model for {lang}: {model_name}")
            except Exception as download_e:
                logging.error(f"Failed to download and load NLP model for {lang}: {download_e}")
                nlp_models[lang] = None
    return nlp_models[lang]

# Google検索（非同期）
async def google_search_async(query, lang, session, num_results=3):
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        logging.warning("Google APIキーが設定されていません。")
        return []
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": num_results,
        "lr": f"lang_{lang}"
    }
    try:
        async with session.get("https://www.googleapis.com/customsearch/v1", params=params) as res:
            res.raise_for_status()
            items = (await res.json()).get("items", [])
            return [{"title": i.get("title"), "link": i.get("link"), "snippet": i.get("snippet"), "source": "Google", "rank": idx + 1} for idx, i in enumerate(items)]
    except Exception as e:
        logging.error(f"Google検索エラー: {e}")
        return []

# Bing検索（非同期）
async def bing_search_async(query, lang, session, num_results=3):
    if not BING_API_KEY:
        logging.warning("Bing APIキーが設定されていません。")
        return []
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "mkt": f"{lang}-{lang.upper()}", "count": num_results}
    try:
        async with session.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params) as res:
            res.raise_for_status()
            items = (await res.json()).get("webPages", {}).get("value", [])
            return [{"title": i.get("name"), "link": i.get("url"), "snippet": i.get("snippet"), "source": "Bing", "rank": idx + 1} for idx, i in enumerate(items)]
    except Exception as e:
        logging.error(f"Bing検索エラー: {e}")
        return []

# X Post検索（非同期）
async def x_post_search_async(query, lang, session, num_results=3):
    if not X_API_KEY:
        logging.warning("X APIキーが設定されていません。")
        return []
    headers = {"Authorization": f"Bearer {X_API_KEY}"}
    params = {"query": query, "lang": lang, "count": num_results}
    try:
        async with session.get("https://api.twitter.com/2/tweets/search/recent", headers=headers, params=params) as res:
            res.raise_for_status()
            data = await res.json()
            tweets = data.get("data", [])
            users = data.get("includes", {}).get("users", [])
            user_map = {user["id"]: user["username"] for user in users}
            return [{
                "title": user_map.get(t.get("author_id"), "Unknown") + "の投稿",
                "link": f"https://twitter.com/{user_map.get(t.get('author_id'), 'unknown')}/status/{t.get('id')}",
                "snippet": t.get("text", ""),
                "source": "X",
                "rank": idx + 1
            } for idx, t in enumerate(tweets)]
    except Exception as e:
        logging.error(f"X Post検索エラー: {e}")
        return []

# FAQ応答生成 (デフォルトでflan-t5-largeを使用)
def generate_faq_answer(query, faq_model_name=DEFAULT_FAQ_MODEL):
    model = load_model(faq_model_name, faq_models, AutoModelForSeq2SeqLM)
    tokenizer = load_tokenizer(faq_model_name, faq_models)
    if not model or not tokenizer:
        return "FAQ応答モデルの読み込みに失敗しました。"
    try:
        inputs = tokenizer(f"question: {query} context:", return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_length=150, num_beams=5, early_stopping=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"FAQ応答生成エラー: {e}")
        return "FAQの応答に失敗しました。"

# 要約 (デフォルトでbart-large-cnnを使用)
def summarize(text, lang, summary_model_name=DEFAULT_SUMMARY_MODEL):
    model = load_model(summary_model_name, summarizer_models, AutoModelForSeq2SeqLM)
    tokenizer = load_tokenizer(summary_model_name, summarizer_models)
    if not model or not tokenizer:
        return ""
    try:
        inputs = tokenizer(text[:1024], return_tensors="pt", truncation=True).to(model.device)
        outputs = model.generate(**inputs, max_length=150, min_length=30, num_beams=4, early_stopping=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logging.error(f"要約生成エラー: {e}")
        return "要約に失敗しました。"

# クエリ解析 (名詞と動詞を抽出)
def analyze_query(query, lang):
    try:
        doc = load_nlp_model(lang)(query)
        keywords = [t.text for t in doc if t.pos_ in ['NOUN', 'VERB']]
        return ' '.join(keywords)
    except Exception as e:
        logging.error(f"クエリ解析エラー: {e}")
        return query

# 表示テキスト (多言語対応)
def get_text(key, lang):
    texts = {
        "ja": {"ai_summary": "AIによる概要", "faq": "FAQ応答", "no_results": "結果が見つかりませんでした。"},
        "en": {"ai_summary": "AI Summary", "faq": "FAQ Response", "no_results": "No results found."}
    }
    return texts.get(lang, texts['ja']).get(key, key)

# Reciprocal Rank Fusion (RRF) を用いたランキング (多様性を考慮)
def rrf_rank(results, k=60):
    ranked_results = {}
    for result in results:
        if result['link'] not in ranked_results:
            ranked_results[result['link']] = result
            ranked_results[result['link']]['rrf_score'] = 0
        ranked_results[result['link']]['rrf_score'] += 1 / (k + result['rank'])

    sorted_results = sorted(ranked_results.values(), key=lambda x: x['rrf_score'], reverse=True)
    return sorted_results

# スコア付け＆統合 (RRF を適用)
def rank_and_merge_results(query, all_results):
    # 各検索エンジンの結果を分離
    google_results = [r for r in all_results if r['source'] == 'Google']
    bing_results = [r for r in all_results if r['source'] == 'Bing']
    x_results = [r for r in all_results if r['source'] == 'X']

    # RRF を適用してランキング
    ranked_google = rrf_rank(google_results)
    ranked_bing = rrf_rank(bing_results)
    ranked_x = rrf_rank(x_results)

    # 全ての結果を結合して再度 RRF で最終ランキング (より多様性を重視)
    all_ranked = rrf_rank(ranked_google + ranked_bing + ranked_x)

    # スコアがない場合は、元の順序を維持
    for i, res in enumerate(all_ranked):
        res['final_rank'] = i + 1
    return all_ranked

# 重複排除 (リンクとスニペットの内容を比較)
def deduplicate_results(results):
    seen_links = set()
    seen_content = set()
    deduped = []
    for r in results:
        if r["link"] not in seen_links and r["snippet"] not in seen_content:
            seen_links.add(r["link"])
            seen_content.add(r["snippet"])
            deduped.append(r)
    return deduped

# 非同期検索の実行 (選択された検索エンジンのみ実行)
async def run_searches(query, lang, search_engines, num_results):
    async with aiohttp.ClientSession() as session:
        tasks = []
        if "google" in search_engines and GOOGLE_API_KEY and GOOGLE_CSE_ID:
            tasks.append(google_search_async(query, lang, session, num_results))
        if "bing" in search_engines and BING_API_KEY:
            tasks.append(bing_search_async(query, lang, session, num_results))
        if "x" in search_engines and X_API_KEY:
            tasks.append(x_post_search_async(query, lang, session, num_results))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        processed_results = []
        for res in results:
            if isinstance(res, Exception):
                logging.error(f"検索エラーが発生しました: {res}")
            else:
                processed_results.extend(res)
        return processed_results

# メイン処理 (ハイブリッド検索)
def hybrid_search(query, search_engines=DEFAULT_SEARCH_ENGINES, num_results=3, summary_model_name=DEFAULT_SUMMARY_MODEL, ranker_model_name=DEFAULT_RANKER_MODEL, faq_model_name=DEFAULT_FAQ_MODEL):
    # キャッシュ確認 (検索設定も考慮)
    lang = detect(query)
    cache_key = f"{query}_{lang}_{'_'.join(sorted(search_engines))}_{num_results}_{summary_model_name}_{ranker_model_name}_{faq_model_name}"
    if cache_key in cache:
        logging.info(f"Cache hit for query: {query} ({lang}) with settings: {cache_key}")
        return cache[cache_key]

    query_keywords = analyze_query(query, lang)

    # 非同期検索
    loop = asyncio.get_event_loop()
    raw_results = loop.run_until_complete(run_searches(query_keywords, lang, search_engines, num_results))

    # 結果のランキングと統合 (RRF を適用)
    ranked_results = rank_and_merge_results(query, raw_results)
    ranked_results = deduplicate_results(ranked_results)

    # FAQ生成（同期処理）
    max_workers = min(multiprocessing.cpu_count(), 4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_faq = executor.submit(generate_faq_answer, query, faq_model_name)
        faq = future_faq.result()

    # 要約
    joined_snippets = ' '.join([r['snippet'] for r in ranked_results if r['snippet']])
    summary = summarize(joined_snippets, lang, summary_model_name)

    # HTML生成
    if not ranked_results:
        result = f"<p>{get_text('no_results', lang)}</p>"
    else:
        html = f"<div>"
        if summary:
            html += f"<h3>{get_text('ai_summary', lang)}</h3><p>{summary}</p>"
        if faq and faq != "FAQの応答に失敗しました。":
            html += f"<h3>{get_text('faq', lang)}</h3><p>{faq}</p><hr>"
        for r in ranked_results:
            html += f"""
            <div style='margin-bottom:1em; border-left: 3px solid #eee; padding-left: 1em;'>
                <b><a href='{r['link']}' target='_blank' style='text-decoration: none;'>{r['title']}</a></b>
                <small>({r['source']})</small><br>
                <p style='margin-top: 0.5em; color: #555;'>{r['snippet']}</p>
            </div>
            """
        html += "</div>"
        result = html

    # キャッシュに保存
    cache[cache_key] = result
    logging.info(f"Cache set for query: {query} ({lang}) with settings: {cache_key}")
    return result

# Gradio UI
with gr.Blocks() as iface:
    gr.Markdown("# 高速・高精度 マルチAI＆検索ハイブリッドシステム (オープンソース公開版)")
    gr.Markdown("Google + Bing + X Post + FAQ応答を高性能AIで統合し、多様性と情報源の透明性を意識して表示")
    query_input = gr.Textbox(lines=2, placeholder="例: オープンソースAIの最新動向は？")
    with gr.Row():search_engine_checkboxes = gr.CheckboxGroup(["google", "bing", "x"], label="検索エンジン (オプション)", value=DEFAULT_SEARCH_ENGINES)
        num_results_slider = gr.Slider(minimum=1, maximum=10, step=1, value=3, label="検索結果数 (オプション)")
    with gr.Accordion("詳細設定 (オプション)", open=False):
        summary_model_dropdown = gr.Dropdown([DEFAULT_SUMMARY_MODEL, "facebook/bart-large-cnn", "google/pegasus-large"], label="要約モデル", value=DEFAULT_SUMMARY_MODEL)
        ranker_model_dropdown = gr.Dropdown([DEFAULT_RANKER_MODEL, "cross-encoder/ms-marco-large-v1"], label="ランキングモデル", value=DEFAULT_RANKER_MODEL)
        faq_model_dropdown = gr.Dropdown([DEFAULT_FAQ_MODEL, "google/flan-t5-large", "gpt2"], label="FAQモデル", value=DEFAULT_FAQ_MODEL)
    search_button = gr.Button("検索")
    output_area = gr.HTML()

    search_button.click(
        hybrid_search,
        inputs=[
            query_input,
            search_engine_checkboxes,
            num_results_slider,
            summary_model_dropdown,
            ranker_model_dropdown,
            faq_model_dropdown
        ],
        outputs=output_area
    )

if __name__ == "__main__":
    iface.launch()
