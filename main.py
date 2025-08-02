import discord
from discord import app_commands
from discord.ext import commands
import json

# Botの初期化
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# 自分のサーバーID（右クリック → IDコピー）
GUILD_ID = discord.Object(id=1234567890)  # ← ここにサーバーID

# Kanjiデータを読み込む
with open("all_kanji.json", encoding="utf-8") as f:
    kanji_data = json.load(f)

@bot.event
async def on_ready():
    print(f"✅ ログイン成功: {bot.user}")

    # 開発用：ギルド限定でコマンド同期（即時反映）
    await tree.sync(guild=GUILD_ID)

    print("✅ ギルドコマンドを同期しました")

# /unicode コマンド
@tree.command(name="unicode", description="漢字のUnicodeを表示", guild=GUILD_ID)
@app_commands.describe(char="漢字1文字")
async def unicode_command(interaction: discord.Interaction, char: str):
    try:
        if len(char) != 1:
            await interaction.response.send_message("⚠️ 1文字だけ入力してください", ephemeral=True)
            return

        entry = kanji_data.get(char)
        if entry and entry.get("unicode"):
            codepoint = f"U+{entry['unicode'].upper()}"
        else:
            codepoint = f"U+{ord(char):04X}"  # JSONにない場合はordで代替

        await interaction.response.send_message(f"「{char}」のUnicode: {codepoint}")

    except Exception as e:
        print(f"❌ /unicode エラー: {e}")

# /radical コマンド
@tree.command(name="radical", description="漢字の部首を表示", guild=GUILD_ID)
@app_commands.describe(char="漢字1文字")
async def radical_command(interaction: discord.Interaction, char: str):
    try:
        if len(char) != 1:
            await interaction.response.send_message("⚠️ 1文字だけ入力してください", ephemeral=True)
            return

        entry = kanji_data.get(char)
        radical = entry.get("radical") if entry else None

        if radical:
            await interaction.response.send_message(f"「{char}」の部首は {radical} です。")
        else:
            await interaction.response.send_message(f"「{char}」の部首情報は見つかりませんでした。", ephemeral=True)

    except Exception as e:
        print(f"❌ /radical エラー: {e}")

# /stroke コマンド
@tree.command(name="stroke", description="漢字の画数を表示", guild=GUILD_ID)
@app_commands.describe(char="漢字1文字")
async def strokes_command(interaction: discord.Interaction, char: str):
    try:
        if len(char) != 1:
            await interaction.response.send_message("⚠️ 1文字だけ入力してください", ephemeral=True)
            return

        entry = kanji_data.get(char)
        stroke = entry.get("stroke") if entry else None

        if stroke is not None:
            await interaction.response.send_message(f"「{char}」の画数は {stroke} 画です。")
        else:
            await interaction.response.send_message(f"「{char}」の画数情報は見つかりませんでした。", ephemeral=True)

    except Exception as e:
        print(f"❌ /stroke エラー: {e}")

# /info コマンド
@tree.command(name="info", description="漢字の情報をまとめて表示", guild=GUILD_ID)
@app_commands.describe(char="漢字1文字")
async def info_command(interaction: discord.Interaction, char: str):
    try:
        if len(char) != 1:
            await interaction.response.send_message("⚠️ 1文字だけ入力してください", ephemeral=True)
            return

        entry = kanji_data.get(char)
        if not entry:
            await interaction.response.send_message(f"「{char}」の情報は見つかりませんでした。", ephemeral=True)
            return

        # それぞれの情報を取り出す（なければ "不明"）
        unicode_str = f"U+{entry['unicode'].upper()}" if entry.get("unicode") else "不明"
        radical = entry.get("radical") or "不明"
        stroke = entry.get("stroke")
        stroke_str = f"{stroke} 画" if stroke is not None else "不明"

        # メッセージを構築
        message = (
            f"「{char}」の情報：\n"
            f"・Unicode: {unicode_str}\n"
            f"・部首: {radical}\n"
            f"・画数: {stroke_str}"
        )

        await interaction.response.send_message(message)

    except Exception as e:
        print(f"❌ /info エラー: {e}")

# /by_unicode コマンド
@tree.command(name="by_unicode", description="Unicodeから漢字を表示", guild=GUILD_ID)
@app_commands.describe(code="Unicode（例: 4EBA または 4eba）")
async def char_command(interaction: discord.Interaction, code: str):
    try:
        # 入力を大文字化して0埋め（例: "4eba" → "04EBA"）
        code = code.strip().lower().zfill(5)
        
        # 辞書を走査して一致する文字を探す
        for char, entry in kanji_data.items():
            if entry.get("unicode", "").lower() == code:
                await interaction.response.send_message(f"U+{code.upper()} → 「{char}」")
                return

        await interaction.response.send_message(f"U+{code.upper()} に該当する文字は見つかりませんでした。", ephemeral=True)

    except Exception as e:
        print(f"❌ /by_unicode エラー: {e}")

# by_radical コマンド
@tree.command(name="by_radical", description="指定した部首を含む漢字を列挙", guild=GUILD_ID)
@app_commands.describe(radical="部首（例: 木, 金）")
async def kanji_by_radical(interaction: discord.Interaction, radical: str):
    try:
        if len(radical.strip()) == 0:
            await interaction.response.send_message("部首を1文字以上で入力してください", ephemeral=True)
            return

        matches = [char for char, entry in kanji_data.items() if entry.get("radical") == radical]

        if matches:
            # 多すぎると長すぎるため、制限をかける
            max_chars = 1500
            message = f"{radical} を含む漢字（{len(matches)}件）：\n" + ", ".join(matches)
            if len(message) > max_chars:
                message = message[:max_chars] + " ..."
            await interaction.response.send_message(message)
        else:
            await interaction.response.send_message(f"「{radical}」の部首を含む漢字は見つかりませんでした。", ephemeral=True)

    except Exception as e:
        print(f"❌ /by_radical エラー: {e}")

# /by_stroke コマンド
@tree.command(name="by_stroke", description="指定した画数の漢字を列挙", guild=GUILD_ID)
@app_commands.describe(count="画数（整数）")
async def kanji_by_stroke(interaction: discord.Interaction, count: int):
    try:
        if count < 1:
            await interaction.response.send_message("1画以上を指定してください", ephemeral=True)
            return

        matches = [char for char, entry in kanji_data.items() if entry.get("stroke") == count]

        if matches:
            # 多すぎるとDiscordの制限に引っかかるので制限付きで表示
            max_chars = 1500  # 合計文字数制限
            message = f"{count}画の漢字（{len(matches)}件）：\n" + ", ".join(matches)
            if len(message) > max_chars:
                message = message[:max_chars] + " ..."
            await interaction.response.send_message(message)
        else:
            await interaction.response.send_message(f"{count}画の漢字は見つかりませんでした。", ephemeral=True)

    except Exception as e:
        print(f"❌ /by_stroke エラー: {e}")

# トークンをここに貼って実行
bot.run("qwerty") # ← ここにbotトークン
