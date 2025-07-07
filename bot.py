import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 설정값들
RAMI_ROLE_NAME = "라미"  # 관리자 역할명
MALE_ROLE_NAME = "남자"  # 남자 역할명
FEMALE_ROLE_NAME = "여자"  # 여자 역할명

# 첫 번째 안내문구
FIRST_MESSAGE = """관리자와 개인 대화가 가능합니다!
5초 내로 적응 상태 확인 메시지를 드릴 예정입니다. 서버 규칙을 확인하시고 편안하게 이용해주세요! 심심해서 들어온거면 관리진들이 불러줄 때 빨리 답장 하고 부르면 음챗방 오셈 답도 안하고 활동 안할거면 걍 딴 서버나 가라 그런 새 끼 받아주는 서버 아님"""

# 두 번째 안내문구 (나중에 수정 예정)
SECOND_MESSAGE = "두 번째 안내문구입니다. (나중에 수정 예정)"

class AdminButtons(discord.ui.View):
    def __init__(self, channel, member):
        super().__init__(timeout=None)
        self.channel = channel
        self.member = member
    
    @discord.ui.button(label='삭제', style=discord.ButtonStyle.danger, emoji='🗑️')
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 라미 역할 확인
        rami_role = discord.utils.get(interaction.guild.roles, name=RAMI_ROLE_NAME)
        if rami_role not in interaction.user.roles:
            await interaction.response.send_message("권한이 없습니다.", ephemeral=True)
            return
        
        # 채널 삭제
        await self.channel.delete()
        await interaction.response.send_message("비공개 방이 삭제되었습니다.", ephemeral=True)
    
    @discord.ui.button(label='보존', style=discord.ButtonStyle.success, emoji='💾')
    async def preserve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 라미 역할 확인
        rami_role = discord.utils.get(interaction.guild.roles, name=RAMI_ROLE_NAME)
        if rami_role not in interaction.user.roles:
            await interaction.response.send_message("권한이 없습니다.", ephemeral=True)
            return
        
        # 멤버가 모든 채팅방을 볼 수 있도록 권한 수정
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(self.member, read_messages=True)
        
        await interaction.response.send_message("보존되었습니다. 이제 모든 채팅방을 볼 수 있습니다.", ephemeral=True)

class UserButtons(discord.ui.View):
    def __init__(self, channel, member):
        super().__init__(timeout=None)
        self.channel = channel
        self.member = member
    
    @discord.ui.button(label='삭제', style=discord.ButtonStyle.danger, emoji='🗑️')
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 본인 확인
        if interaction.user != self.member:
            await interaction.response.send_message("본인만 누를 수 있습니다.", ephemeral=True)
            return
        
        # 채널 삭제
        await self.channel.delete()
        await interaction.response.send_message("비공개 방이 삭제되었습니다.", ephemeral=True)
    
    @discord.ui.button(label='보존', style=discord.ButtonStyle.success, emoji='💾')
    async def preserve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 본인 확인
        if interaction.user != self.member:
            await interaction.response.send_message("본인만 누를 수 있습니다.", ephemeral=True)
            return
        
        # 성별에 따른 이름 변경
        male_role = discord.utils.get(interaction.guild.roles, name=MALE_ROLE_NAME)
        female_role = discord.utils.get(interaction.guild.roles, name=FEMALE_ROLE_NAME)
        
        new_nick = self.member.display_name
        
        if male_role in self.member.roles:
            if not new_nick.startswith("(단팥빵)"):
                new_nick = f"(단팥빵) {new_nick}"
        elif female_role in self.member.roles:
            if not new_nick.startswith("(메론빵)"):
                new_nick = f"(메론빵) {new_nick}"
        
        try:
            await self.member.edit(nick=new_nick)
            await interaction.response.send_message("보존되었습니다. 닉네임이 변경되었습니다.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("닉네임 변경 권한이 없습니다.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'{bot.user} 봇이 준비되었습니다!')
    print(f'서버 수: {len(bot.guilds)}')

@bot.event
async def on_member_join(member):
    guild = member.guild
    
    # 라미 역할을 가진 관리자 찾기
    rami_role = discord.utils.get(guild.roles, name=RAMI_ROLE_NAME)
    if not rami_role:
        print(f"'{RAMI_ROLE_NAME}' 역할을 찾을 수 없습니다.")
        return
    
    rami_members = [m for m in guild.members if rami_role in m.roles and m.bot == False]
    if not rami_members:
        print("라미 역할을 가진 관리자가 없습니다.")
        return
    
    # 첫 번째 라미 관리자 선택
    admin = rami_members[0]
    
    # 비공개 채널 생성 (완전 비공개)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            read_messages=False,
            send_messages=False,
            view_channel=False
        ),
        member: discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
            view_channel=True
        ),
        admin: discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
            view_channel=True
        )
    }
    
    # 라미 역할 전체에게도 권한 부여
    if rami_role:
        overwrites[rami_role] = discord.PermissionOverwrite(
            read_messages=True,
            send_messages=True,
            view_channel=True
        )
    
    channel_name = f"입장-{member.display_name}-{datetime.now().strftime('%m%d-%H%M')}"
    private_channel = await guild.create_text_channel(
        name=channel_name,
        overwrites=overwrites,
        category=None
    )
    
    # 새 멤버 권한 설정: 음성채널만 보이게
    for channel in guild.text_channels:
        if channel != private_channel:
            await channel.set_permissions(member, read_messages=False)
    
    for channel in guild.voice_channels:
        await channel.set_permissions(member, view_channel=True)
    
    # 환영 채널 삭제 (만약 다른 봇이 생성했다면)
    welcome_channels = [ch for ch in guild.text_channels if ch.name.startswith(f"환영-{member.display_name}")]
    for welcome_channel in welcome_channels:
        try:
            await welcome_channel.delete()
            print(f"환영 채널 삭제됨: {welcome_channel.name}")
        except discord.Forbidden:
            print(f"환영 채널 삭제 권한 없음: {welcome_channel.name}")
        except Exception as e:
            print(f"환영 채널 삭제 중 오류: {e}")
    
    # 첫 번째 안내문구 전송
    embed1 = discord.Embed(
        title="🎉 서버에 오신 것을 환영합니다!",
        description=FIRST_MESSAGE,
        color=0x00ff00
    )
    
    admin_view = AdminButtons(private_channel, member)
    message1 = await private_channel.send(f"{member.mention} {admin.mention}", embed=embed1, view=admin_view)
    
    # 5초 후 두 번째 안내문구 전송
    await asyncio.sleep(5)
    
    embed2 = discord.Embed(
        title="📋 추가 안내사항",
        description=SECOND_MESSAGE,
        color=0x0099ff
    )
    
    user_view = UserButtons(private_channel, member)
    message2 = await private_channel.send(embed=embed2, view=user_view)

# 봇 실행
if __name__ == "__main__":
    # 환경변수에서 토큰 가져오기
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("DISCORD_TOKEN 환경변수를 설정해주세요.")
        print("또는 아래 라인의 주석을 해제하고 직접 토큰을 입력하세요.")
        # TOKEN = "여기에_봇_토큰_입력"
    
    bot.run(TOKEN)
