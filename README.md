# Sigma Awards 選出傾向レポート

[The Sigma Awards](https://sigmaawards.org) の2020〜2026年の全応募3,899件をもとに、ショートリスト以上に選ばれた作品の特徴を調べたレポートです。日本から応募を準備する人のための資料として、Data Visualization Japan が公開しています。

公開ページ: https://datavisualizationjapan.github.io/sigma-awards-report/

作品を1件ずつ探す場合は、[Sigma Awards エントリー一覧](https://sigma-awards.data-visualization.jp/) を使ってください。

## 主な結果

- ポートフォリオ応募は、平均の1.65倍選ばれています（482件中113件）
- 複数編集部の協働は1.53倍、衛星画像は1.51倍、公開情報調査（OSINT）は1.36倍です
- OSINTを挙げる応募は2020年の3.2%から2026年の22.9%に増えました
- 組織規模による差は誤差の範囲で、受賞は小規模39件、大規模37件です
- 日本からは38件が応募し、ショートリストは4件、受賞は0件です

「◯倍」は、年ごとの選出率の違いをならしたうえでの平均との比です。タグとツールは応募者の自己申告で、比は相関を示すものです。計算方法と注意点はページ末尾にあります。

## 構成

| パス | 内容 |
|---|---|
| `index.html` | 公開ページ（集計結果を埋め込んだ単一ファイル） |
| `analyze.py` | 集計。[DataVisualizationJapan/sigma-awards](https://github.com/DataVisualizationJapan/sigma-awards) の `public/data/` を読み、`stats.json` を出力 |
| `stats.json` | 集計結果 |
| `template.html`, `build.py` | `stats.json` を埋め込んで `index.html` を生成 |

## 更新のしかた

```bash
git clone --depth 1 https://github.com/DataVisualizationJapan/sigma-awards ../sigma-awards
python3 analyze.py ../sigma-awards stats.json
python3 build.py
```

ページ冒頭と要点の一部の文は固定の文面です。年度が増えたときは `template.html` の文面も見直してください。

## データとライセンス

- 応募データ: [The Sigma Awards projects data](https://github.com/Sigma-Awards/The-Sigma-Awards-projects-data)（The Sigma Awards / Global Investigative Journalism Network, CC BY-NC-SA 4.0）
- このレポートの集計結果と図も、同じ [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) で提供します。利用時は出典の表示、非営利、同じ条件での共有が必要です
- Data Journalism Awards（2012〜2019年）の記録は、保存資料で確認できる受賞・候補のみです


## アクセス解析

共通仕様は [docs/analytics.md](docs/analytics.md) を参照してください。測定IDと本番ホスト名は analytics.json に集約しています。GA管理画面の履歴変更による自動ページビューとサイト内検索の自動収集を無効にしてから公開してください。検索語を含むURLパラメータのデータ編集設定も必要です。
