import discord
from discord import app_commands
from discord.ext import commands
import requests
from datetime import datetime

# ==========================================================
# KONFIGURASI
# ==========================================================
TOKEN = 'input your token developer discord'
SERVER_LIST = {
    "ime": "http://main.imeroleplay.com:30120",
    "inter": "http://inter.imeroleplay.com:30120",
    "idp": "http://idp-roleplay.com:30120"
}
WA_LINK = 'https://discord.com/users/941381774003564615'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================================
# FUNGSI UTAMA
# ==========================================================
def create_embed(title, color):
    embed = discord.Embed(title=title, color=color, timestamp=datetime.now())
    embed.set_footer(text="© 2026 Lucky - IC. UCOK UCOK", icon_url=bot.user.display_avatar.url)
    return embed

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Hi GANTENG ,Bot READY ya Bosq!")
    print("GUNAKAN DENGAN BIJAK & JANGAN MIXING YA Bosq!")

# ==========================================================
# PERINTAH SLASH
# ==========================================================

@bot.tree.command(name="help", description="Daftar perintah bot")
async def help(interaction: discord.Interaction):
    text = "🤖 **PANDUAN BOT:** /status, /cari, /info,/help"
    await interaction.response.send_message(text, ephemeral=True)

@bot.tree.command(name="status", description="Cek status server")
async def status(interaction: discord.Interaction, nama: str):
    await interaction.response.defer()
    try:
        data = requests.get(f"{SERVER_LIST[nama.lower()]}/players.json", timeout=5).json()
        embed = create_embed(f"📊 Server {nama.upper()}", discord.Color.blurple())
        embed.add_field(name="Pemain Online", value=f"`{len(data)}`", inline=True)
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("❌ Server tidak terdeteksi.")

@bot.tree.command(name="info", description="Cek detail teknis server")
async def info(interaction: discord.Interaction, nama: str):
    await interaction.response.defer()
    try:
        info_data = requests.get(f"{SERVER_LIST[nama.lower()]}/info.json", timeout=5).json()
        embed = create_embed(f"ℹ️ Detail Server: {nama.upper()}", discord.Color.green())
        embed.add_field(name="KAPASITAS SLOT", value=f"`{info_data.get('vars', {}).get('sv_maxClients', '??')}`", inline=True)
        embed.add_field(name="JUMLAH SCRIPT", value=f"`{len(info_data.get('resources', []))}`", inline=True)
        embed.add_field(name="SERVER BUILD", value=f"`{info_data.get('server', 'Unknown')}`", inline=True)
        await interaction.followup.send(embed=embed)
    except:
        await interaction.followup.send("❌ Gagal mengambil detail info server.")

@bot.tree.command(name="cari", description="Cari pemain dengan format pro")
async def cari(interaction: discord.Interaction, nama_server: str, nama_pemain: str):
    await interaction.response.defer()
    try:
        players = requests.get(f"{SERVER_LIST[nama_server.lower()]}/players.json", timeout=5).json()
        hasil = [p for p in players if nama_pemain.lower() in p['name'].lower()]
        
        if not hasil:
            await interaction.followup.send("❌ Tidak ditemukan.")
            return

        embed = create_embed(f"🔍 HASIL: {nama_pemain.upper()}", discord.Color.blurple())
        display_text = ""
        for idx, p in enumerate(hasil[:5]):
            ping = p.get('ping', 0)
            status_ping = "🟢 HIJAU" if ping < 100 else ("🟡 KUNING" if ping < 300 else "🔴 MERAH")
            display_text += (
                f"**[NO {idx+1}]**\n"
                f"**NAMA:** {p['name']}\n"
                f"**ID:** {p['id']}\n"
                f"**JARINGAN:** {status_ping} {ping}MS\n"
                f"----------------------------\n"
            )
        
        embed.add_field(name="DETAIL PEMAIN", value=display_text, inline=False)
        
        view = discord.ui.View()
        button = discord.ui.Button(label="Hubungi Admin", url=WA_LINK, style=discord.ButtonStyle.link)
        view.add_item(button)
        
        await interaction.followup.send(embed=embed, view=view)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(TOKEN)