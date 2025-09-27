

# Made By Younes Aka : Old
import discord
import json
import os
from discord.ext import commands
from discord import app_commands
import asyncio
from dotenv import load_dotenv

MESSAGES_JSON = "messages.json"
MODERATOR_ROLE_ID = 1380830184567078943
APPLICATION_CHANNEL_ID = 1399540680107364486
ALLOWED_USER_ID = 241597878944923648

MUSIC_BOTS = {
    412347553141751808: "m!play or m!p",
    412347780841865216: "m!play or m!p",
    411916947773587456: "m!play or m!p",
    412347257233604609: "m!play or m!p",
    451379187031343104: "!play",
    944016826751389717: "+play",
    945683386100514827: "/play",
}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)


def save_message(key, message_id):
    data = {}
    if os.path.exists(MESSAGES_JSON):
        with open(MESSAGES_JSON, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {}
    data[key] = message_id
    with open(MESSAGES_JSON, "w") as f:
        json.dump(data, f)

def load_message(key):
    if not os.path.exists(MESSAGES_JSON):
        return None
    with open(MESSAGES_JSON, "r") as f:
        data = json.load(f)
        return data.get(key)


class ApplicationView(discord.ui.View):
    def __init__(self, user, role_id=None, is_partner=False):
        super().__init__(timeout=None)
        self.user = user
        self.role_id = role_id
        self.is_partner = is_partner

    async def disable_buttons(self, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="accept_button")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("You are not authorized to accept this application.", ephemeral=True)
            return

        if not self.is_partner and self.role_id:
            role = interaction.guild.get_role(self.role_id)
            if role:
                await self.user.add_roles(role)
                try:
                    await self.user.send(f"✅ You have been accepted as **{role.name}** in **{interaction.guild.name}**!")
                except:
                    print(f"Couldn't DM {self.user}.")
        else:
            try:
                await self.user.send(f"✅ You have been accepted as a **Partner** in **{interaction.guild.name}**!")
            except:
                print(f"Couldn't DM {self.user}.")

        await interaction.response.send_message(f"{self.user.mention} has been accepted.", ephemeral=False)
        await self.disable_buttons(interaction)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.danger, custom_id="deny_button")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != ALLOWED_USER_ID:
            await interaction.response.send_message("You are not authorized to deny this application.", ephemeral=True)
            return

        await interaction.response.send_message(f"{self.user.mention}'s application has been denied.", ephemeral=False)
        await self.disable_buttons(interaction)

class Moderator(discord.ui.Modal, title="Apply for Moderator"):
    name = discord.ui.TextInput(label="Age + Smitk Complet", placeholder="Troll = Mute", required=True)
    age = discord.ui.TextInput(label="Elash A Nkhtarok Nta Bdbt Bach Gha Tfidna ?", required=True)
    about = discord.ui.TextInput(label="Elax Khtariti Server Dialna Ou Mchi Wahd Akhr", placeholder="Take Your Time", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thanks for applying!", ephemeral=True)
        try:
            channel = await bot.fetch_channel(APPLICATION_CHANNEL_ID)
            embed = discord.Embed(title="**📝 New Moderator Application**")
            embed.description = f"👤 Applicant: {interaction.user.mention}"
            embed.add_field(name="👤 Name Wlage", value=str(self.name), inline=False)
            embed.add_field(name="📘 Why You?", value=str(self.age), inline=False)
            embed.add_field(name="🧭 Why Our Server?", value=str(self.about), inline=False)
            embed.set_footer(text=f"User ID: {interaction.user.id}",
                             icon_url="https://cdn.discordapp.com/icons/1172194616192278598/6f999bf179bb46471cef30bd67cdb53b.png?size=1024")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            view = ApplicationView(user=interaction.user, role_id=MODERATOR_ROLE_ID, is_partner=False)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            print(f"Failed to send moderator application: {e}")

class Partnerr(discord.ui.Modal, title="Apply for Partner"):
    name = discord.ui.TextInput(label="ID D Server", required=True)
    age = discord.ui.TextInput(label="Elash Khtaritina?", required=True)
    about = discord.ui.TextInput(label="Chno Mhtaj Mn Had Lpartner?", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thanks for applying!", ephemeral=True)
        try:
            channel = await bot.fetch_channel(APPLICATION_CHANNEL_ID)
            embed = discord.Embed(title="**📝 New Partner Application**")
            embed.description = f"👤 Applicant: {interaction.user.mention}"
            embed.add_field(name="🏠 Server ID", value=str(self.name), inline=False)
            embed.add_field(name="💬 Why Us?", value=str(self.age), inline=False)
            embed.add_field(name="📋 What You Need?", value=str(self.about), inline=False)
            embed.set_footer(text=f"User ID: {interaction.user.id}",
                             icon_url="https://cdn.discordapp.com/icons/1172194616192278598/6f999bf179bb46471cef30bd67cdb53b.png?size=1024")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            view = ApplicationView(user=interaction.user, is_partner=True)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            print(f"Failed to send partner application: {e}")

class Lmehdaoui(discord.ui.Modal, title="Apply for Lmehdaoui"):
    name = discord.ui.TextInput(label="Smitk Complet", required=True)
    age = discord.ui.TextInput(label="Age", required=True)
    tlo7 = discord.ui.TextInput(label="Kfash A T3rf Imta Tlo7 Ou Imta la", required=True)
    news_type = discord.ui.TextInput(label="No3 Dakhbar Li Endk Ou Baghi Tkon Mklf Bihom", required=True)
    why = discord.ui.TextInput(label="Elash BAghi Twli Sahafi", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Thanks for applying!", ephemeral=True)
        try:
            channel = await bot.fetch_channel(APPLICATION_CHANNEL_ID)
            embed = discord.Embed(title="**📝 New Lmehdaoui Application**")
            embed.description = f"👤 Applicant: {interaction.user.mention}"
            embed.add_field(name="👤 Smitk Complet", value=str(self.name), inline=False)
            embed.add_field(name="🎂 Age", value=str(self.age), inline=False)
            embed.add_field(name="🕒 Tlo7", value=str(self.tlo7), inline=False)
            embed.add_field(name="📰 No3 Dakhbar", value=str(self.news_type), inline=False)
            embed.add_field(name="❓ Why", value=str(self.why), inline=False)
            embed.set_footer(text=f"User ID: {interaction.user.id}",
                             icon_url="https://cdn.discordapp.com/icons/1172194616192278598/6f999bf179bb46471cef30bd67cdb53b.png?size=1024")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            view = ApplicationView(user=interaction.user, is_partner=False)
            await channel.send(embed=embed, view=view)
        except Exception as e:
            print(f"Failed to send Lmehdaoui application: {e}")

class ApplyB(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Moderateur', emoji="<:emoji_37:1399554413256904785>", custom_id="apply_moderateur")
    async def mod(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Moderator())

    @discord.ui.button(label='Partnerr', emoji="<:emoji_36:1399554391798976522>", custom_id="apply_partnerr")
    async def partner(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Partnerr())

    @discord.ui.button(label='Lmehdaoui', emoji="<:1000006048:1412819622771822794>", custom_id="apply_lmehdaoui")
    async def lmehdaoui(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Lmehdaoui())

@bot.command()
@commands.has_permissions(administrator=True)
async def applyh(ctx):
    embed = discord.Embed(title="**Partner/Mod Application**")
    embed.description = (
        "<:emoji_72:1400150666407575694>   Our __Team__ Is Now **_accepting_** Applications For **__New Members__**  To Join Our Team!\n"
        "<:emoji_74:1400150727518588938> **Requirements**\n"
        " - Must Be **18 Years** Of Age Or __Older__\n"
        " - For **Partner** You Must Have Over Then __+1500 Members__.\n"
        " - Must Not Have A Lot Of __**Warnings**__ And Be Active In The **Server**\n"
        "<:emoji_72:1400150690495463556> **Application Process** :\n"
        " - To Apply, Click On One Of The Buttons Below This Message\n"
        " - Trolling Or Spamming = 3 Days Mute"
    )
    embed.set_footer(text="Partner/Mod Application | powered by: Old",
                     icon_url="https://cdn.discordapp.com/avatars/1075280690414882906/67ed78e7a263fc3ad298553f78835123.png?size=1024")
    embed.set_author(name="Achraf Sabiri Server",
                     icon_url="https://cdn.discordapp.com/avatars/1172194616192278598/6f999bf179bb46471cef30bd67cdb53b.png?size=1024")
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else "")
    message = await ctx.send(embed=embed, view=ApplyB())
    save_message("apply_message_id", message.id)


class CheckMusicBotsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  

    @discord.ui.button(label="🎵 Check Music Bots", style=discord.ButtonStyle.blurple, custom_id="check_music_bots")
    async def check_bots(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        available = []

        for bot_id, prefix in MUSIC_BOTS.items():
            bot_member = guild.get_member(bot_id)
            if not bot_member:
                continue
            if bot_member.status != discord.Status.offline and not bot_member.voice:
                available.append((bot_member, prefix))

        if available:
            bot, prefix = available[0]
            msg = f"✅ **Available Music Bot:** {bot.mention}\n**Prefix:** `{prefix}`"
        else:
            msg = "❌ **All music bots are currently busy or offline.**"

        await interaction.response.send_message(msg, ephemeral=True) 


@bot.command()
async def checkbots(ctx):
    embed = discord.Embed(
        title="🎷 Music Bot Monitor",
        description=(
            "Welcome to the **Music Bot Availability Checker**!\n\n"
            "- Use this tool to quickly find out if one of our Jockie bots or other music bots is **online and free to join**.\n\n"
            "- Just click the button below — if a bot is available, you'll get its name and prefix!\n\n"
            "🎵 | Whether you're setting the vibe or chilling solo, weve got you covered."
        ),
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url if ctx.guild.icon else "")
    embed.set_footer(
        text="Powered by: Old Server Utilities",
        icon_url="https://cdn.discordapp.com/avatars/1075280690414882906/67ed78e7a263fc3ad298553f78835123.png?size=1024"
    )

    message = await ctx.send(embed=embed, view=CheckMusicBotsView())
    save_message("checkbots_message_id", message.id)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print('✅ Logged in to Discord')

    apply_message_id = load_message("apply_message_id")
    if apply_message_id:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    perms = channel.permissions_for(guild.me)
                    if not perms.read_messages or not perms.read_message_history:
                        continue
                    message = await channel.fetch_message(apply_message_id)
                    await message.edit(view=ApplyB())
                    print(f"✅ Reattached ApplyB view to message {apply_message_id} in {guild.name}")
                    break
                except Exception:
                    continue

    checkbots_message_id = load_message("checkbots_message_id")
    if checkbots_message_id:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    perms = channel.permissions_for(guild.me)
                    if not perms.read_messages or not perms.read_message_history:
                        continue
                    message = await channel.fetch_message(checkbots_message_id)
                    await message.edit(view=CheckMusicBotsView())
                    print(f"✅ Reattached CheckMusicBotsView to message {checkbots_message_id} in {guild.name}")
                    break
                except Exception:
                    continue

@bot.command()
@commands.has_permissions(administrator=True)
async def holidaymods(ctx):
    embed = discord.Embed(
        title="🏝️ Moderator Holiday Application",
        description=(
            "Our **Moderation Team** can now request holidays!\n\n"
            "📝 **Process:**\n"
            " - Click the button below to fill out your holiday request.\n"
            " - Provide your **Full Name**, **Duration**, and **Reason**.\n"
            " - Requests will be reviewed and responded to by the staff.\n\n"
            "⚠️ Note: Abusing this system may result in removal from the moderator team."
        ),
        color=discord.Color.teal()
    )
    embed.set_author(name="Achraf Sabiri Server - Holiday Manager", icon_url=ctx.guild.icon.url if ctx.guild.icon else "")
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/869/869636.png")
    embed.set_footer(text="Holiday Request System | powered by Old")

    # Attach audio file with embed
    file_path = "ropo.mp3"  # make sure this file exists in your bot folder
    if os.path.exists(file_path):
        file = discord.File(file_path, filename="ropo.mp3")
        message = await ctx.send(embed=embed, view=HolidayApplyView(), file=file)
    else:
        message = await ctx.send(embed=embed, view=HolidayApplyView())

    save_message("holidaymods_message_id", message.id)




# ===== Run Bot =====
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
