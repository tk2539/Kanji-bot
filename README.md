# Kanji-bot

## 概要

これはビッグデータを利用した漢字のDiscordのbotです

## 使い方

main.pyにbotを追加したいサーバーのIDとbotのトークンを入れて実行して[Discordのbot管理](https://discord.com/developers/applications)でアプリを作りサーバーに追加すると実行している間のみbotが使えます

## コマンド一覧

- `/unicode` コマンド => 漢字を一文字入れるとUnicodeで返信
- `/radical` コマンド => 漢字を一文字入れると部首で返信
- `/stroke` コマンド => 漢字を一文字入れると画数で返信
- `/info` コマンド => 漢字を一文字入れると上記の三つ全てで返信
- `/by_unicode` コマンド => Unicodeを入れると該当する漢字を返信
- `by_radical` コマンド => 部首を入れると該当する全ての漢字で返信
- `/by_stroke コマンド` => 画数を入れると該当する全ての漢字で返信

## ファイル

- all_kanji.json => 漢字ごとに漢字,部首,ユニコード,画数が収納されている
- main.py => botのコア

## 出典

このデータは KanjiVG プロジェクトの XML ファイルをもとに、
以下の情報を抽出・加工したものです：

- 漢字（element）
- 部首（radical）
- ユニコード（unicode）
- 画数（stroke）

元データ: [KanjiVG GitHub](https://github.com/KanjiVG/kanjivg)

ライセンス: [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)

## このリポジトリの加工内容

- XML を Python スクリプトで解析
- 各漢字のストローク数（画数）を追加
- JSON 形式で保存
