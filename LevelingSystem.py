from _database_objects import User
from discord.ext import commands


class Level:
    def __init__(self):
        self.level1 = 1000
        self.level2 = 1000 + self.level1*(1/4)
        self.level3 = self.level2 + self.level2*(1/4)
        self.level4 = self.level3 + self.level3*(1/4)
        self.level5 = self.level4 + self.level4*(1/4)
        self.level6 = self.level5 + self.level5*(1/4)
        self.level7 = self.level6 + self.level6*(1/4)
        self.level8 = self.level7 + self.level7*(1/4)
        self.level9 = self.level8 + self.level8*(1/4)
        self.level10 = self.level9 + self.level9*(1/4)
        self.level11 = self.level10 + self.level10*(1/4)
        self.level12 = self.level11 + self.level11*(1/4)
        self.level13 = self.level12 + self.level12*(1/4)
        self.level14 = self.level13 + self.level13*(1/4)
        self.level15 = self.level14 + self.level14*(1/4)
        self.level16 = self.level15 + self.level15*(1/4)
        self.level17 = self.level16 + self.level16*(1/4)
        self.level18 = self.level17 + self.level17*(1/4)
        self.level19 = self.level18 + self.level18*(1/4)
        self.level20 = self.level19 + self.level19*(1/4)
        self.level21 = self.level20 + self.level20*(1/4)
        self.level22 = self.level21 + self.level21*(1/4)
        self.level23 = self.level22 + self.level22*(1/4)
        self.level24 = self.level23 + self.level23*(1/4)
        self.level25 = self.level24 + self.level24*(1/4)
        self.level26 = self.level25 + self.level25*(1/4)
        self.level27 = self.level26 + self.level26*(1/4)
        self.level28 = self.level27 + self.level27*(1/4)
        self.level29 = self.level28 + self.level28*(1/4)
        self.level30 = self.level29 + self.level29*(1/4)
        self.level31 = self.level30 + self.level30*(1/4)
        self.level32 = self.level31 + self.level31*(1/4)
        self.level33 = self.level32 + self.level32*(1/4)
        self.level34 = self.level33 + self.level33*(1/4)
        self.level35 = self.level34 + self.level34*(1/4)
        self.level36 = self.level35 + self.level35*(1/4)
        self.level37 = self.level36 + self.level36*(1/4)
        self.level38 = self.level37 + self.level37*(1/4)
        self.level39 = self.level38 + self.level38*(1/4)
        self.level40 = self.level39 + self.level39*(1/4)
        self.level41 = self.level40 + self.level40*(1/4)
        self.level42 = self.level41 + self.level41*(1/4)
        self.level43 = self.level42 + self.level42*(1/4)
        self.level44 = self.level43 + self.level43*(1/4)
        self.level45 = self.level44 + self.level44*(1/4)
        self.level46 = self.level45 + self.level45*(1/4)
        self.level47 = self.level46 + self.level46*(1/4)
        self.level48 = self.level47 + self.level47*(1/4)
        self.level49 = self.level48 + self.level48*(1/4)
        self.level50 = self.level49 + self.level49*(1/4)
        self.level51 = self.level50 + self.level50*(1/4)
        self.level52 = self.level51 + self.level51*(1/4)
        self.level53 = self.level52 + self.level52*(1/4)
        self.level54 = self.level53 + self.level53*(1/4)
        self.level55 = self.level54 + self.level54*(1/4)
        self.level56 = self.level55 + self.level55*(1/4)
        self.level57 = self.level56 + self.level56*(1/4)
        self.level58 = self.level57 + self.level57*(1/4)
        self.level59 = self.level58 + self.level58*(1/4)
        self.level60 = self.level59 + self.level59*(1/4)


class LevelingSystem:
    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        all_members = []
        for server in self.client.servers:
            for member in server.members:
                if member not in all_members:
                    all_members.append(member)
        for member in all_members:
            user = await User.find_by_id(member.id)
            if user is None:
                game_name = None
                if member.game:
                    game_name = member.game.name
                user = User(member.id, member.name, member.nick, game_name, member.top_role.name)
                await user.commit()

    async def get_exp(self, user):
        user.current_exp += 100

    async def level_up(self, user, msg):
        next_level = user.level + 1
        level = Level()
        next_level = eval(f"level.level{next_level}")
        if user.current_exp >= next_level:
            user.level += 1
            await self.client.send_message(msg.channel, f'{user.user_name} LevelUp\nDein Level ist nun {user.level}')

    async def on_message(self, msg):
        content = msg.content
        print(content)
        if not str(content).startswith('!'):
            member = msg.author
            user = await User.find_by_id(member.id)
            await self.get_exp(user)
            await self.level_up(user, msg)
            await user.commit()
            print(f'Name {user.user_name}, exp {user.current_exp}, level {user.level}')

    @commands.command(pass_context=True)
    async def prestige(self, ctx):
        user = await User.find_by_id(ctx.message.author.id)
        if user.level == 60:
            user.level = 0
            user.prestige += 1
            await self.client.send_message(ctx.message.channel, f"{user.user_name}: ist nun Prestige {user.prestige}")
        else:
            await self.client.send_message(ctx.message.channel, f"{user.user_name} Du bist ein richtiger lowBOB dein "
                                                                f"Level reicht für kein Prestige\nExp: "
                                                                f"{user.current_exp}, Level: {user.level}")

    @commands.command(pass_context=True)
    async def mylevel(self, ctx):
        user = await User.find_by_id(ctx.message.author.id)
        if user:
            await self.client.send_message(ctx.message.channel, f'{user.user_name} deine exp sind {user.current_exp} '
                                                                f'und dein Level ist {user.level}')


def setup(client):
    client.add_cog(LevelingSystem(client))
