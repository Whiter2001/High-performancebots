import discord
from discord import app_commands
import re
import datetime

TOKEN = "MTE1MDc0OTQzNzExMTU4Mjc3MQ.GM-uIE.s6MaCKu9L30fyANILePmwIeHTirYGzwlNcxKnU"
SERVER_ID = 1148569449511780444
WELCOME_MESSAGE_CHANNEL_ID = 1148569449511780447

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TARGET_GUILD = discord.Object(id=SERVER_ID)


@client.event
async def on_ready():
    print(f'Login BotName: "{client.user}"')
    await tree.sync(guild=TARGET_GUILD)
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game(name="/help")
    )


@client.event
async def on_message(message):
    if message.guild:
        print(f"> [{message.channel.name}] <{message.author}> {message.content}")
    else:
        print(f"<{message.author}> {message.content}")


@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_MESSAGE_CHANNEL_ID)
    await channel.send(
        embed=discord.Embed(
            title=f"@{member.name} Welcome to Server\nYou Are A Member Of {client.get_guild(SERVER_ID).member_count}"
        )
    )
    print(member)


@client.event
async def on_raw_reaction_add(reaction):
    m = await client.get_channel(reaction.channel_id).fetch_message(reaction.message_id)
    if m.author.id == client.user.id and reaction.emoji.name == "":
        guild = client.get_guild(reaction.guild_id)
        roleID = re.search(r"\d+", m.embeds[0].description.splitlines()[0]).group()
        role = guild.get_role(int(roleID))
        await guild.get_member(reaction.user_id).add_roles(role)


@tree.command(guild=TARGET_GUILD, name="help", description="ヘルプを表示")
async def help_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)

    m = [
        "```",
        "help    : ヘルプを表示します",
        "poll    : 投票を作成します",
        "以下 管理者のみ",
        "verifier: 認証メッセージを作成します",
        "```",
    ]

    await interaction.followup.send("\n".join(m))


@tree.command(guild=TARGET_GUILD, name="poll", description="投票を作成")
@app_commands.describe(
    title="タイトル",
    ans1="回答1",
    ans2="回答2",
    ans3="回答3",
    ans4="回答4",
    ans5="回答5",
    ans6="回答6",
    ans7="回答7",
    ans8="回答8",
)
async def poll_command(
    interaction: discord.Interaction,
    title: str,
    ans1: str,
    ans2: str = None,
    ans3: str = None,
    ans4: str = None,
    ans5: str = None,
    ans6: str = None,
    ans7: str = None,
    ans8: str = None,
):
    await interaction.response.defer(ephemeral=True, thinking=True)

    text = ""
    num = 1
    if ans1 != None:
        text = f"{text}{num}. {ans1}\n"
        num += 1
    if ans2 != None:
        text = f"{text}{num}. {ans2}\n"
        num += 1
    if ans3 != None:
        text = f"{text}{num}. {ans3}\n"
        num += 1
    if ans4 != None:
        text = f"{text}{num}. {ans4}\n"
        num += 1
    if ans5 != None:
        text = f"{text}{num}. {ans5}\n"
        num += 1
    if ans6 != None:
        text = f"{text}{num}. {ans6}\n"
        num += 1
    if ans7 != None:
        text = f"{text}{num}. {ans7}\n"
        num += 1
    if ans8 != None:
        text = f"{text}{num}. {ans8}\n"
        num += 1

    m = await interaction.channel.send(
        embed=discord.Embed(title=title, description=text)
    )
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    for v in reactions[: num - 1]:
        await m.add_reaction(v)

    await interaction.followup.send("Command Success!")


@tree.command(guild=TARGET_GUILD, name="verifier", description="認証メッセージを作成")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    role="付与するロール",
    message="メッセージ",
)
async def verifier_command(
    interaction: discord.Interaction,
    role: discord.Role,
    message: str,
):
    await interaction.response.defer(ephemeral=True, thinking=True)

    m = await interaction.channel.send(
        embed=discord.Embed(title="認証パネル", description=f"## <@&{role.id}>\n{message}")
    )
    await m.add_reaction("✅")

    await interaction.followup.send("Command Success!")


@tree.command(guild=TARGET_GUILD, name="shop", description="今日のショップを表示")
async def verifier_command(
    interaction: discord.Interaction,
):
    await interaction.response.defer(ephemeral=False, thinking=True)

    now = datetime.datetime.today()
    await interaction.followup.send(
        embed=discord.Embed(
            title="Today's Shop",
            url=f"https://bot.fnbr.co/shop-image/fnbr-shop-{now.day}-{now.month}-{now.year}.png",
        ).set_image(
            url=f"https://bot.fnbr.co/shop-image/fnbr-shop-{now.day}-{now.month}-{now.year}.png"
        )
    )

@tree.command(guild=TARGET_GUILD, name="map", description="マップを表示")
async def verifier_command(
    interaction: discord.Interaction,
):
    await interaction.response.defer(ephemeral=False, thinking=True)

    await interaction.followup.send(
        embed=discord.Embed(
            title="Map",
            url=f"https://fortnite-api.com/images/map_ja.png",
        ).set_image(
            url=f"https://fortnite-api.com/images/map_ja.png"
        )
    )
# 起動
client.run(TOKEN)