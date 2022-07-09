import discord
from discord.ext import commands, tasks

from apiclient import discovery
from oauth2client import client, file, tools
import json
from datetime import datetime, timedelta


def authAPI():
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    with open("../secrets/creds.json") as f:
        creds = json.load(f)
    oauth = client.OAuth2Credentials(
        access_token=None,
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        refresh_token=creds["refresh_token"],
        token_expiry=None,
        token_uri=creds["token_uri"],
        user_agent=None,
        revoke_uri=creds["revoke_uri"]
    )

    return discovery.build('forms', 'v1', credentials=oauth, discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)


class notification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not self.checkFormResponses.is_running():
            self.checkFormResponses.start()

        self.SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"

        self.FORM_ID = open("../secrets/secrets.txt").readline().rstrip()

        with open("../secrets/lastChecked.txt", 'r+t') as f:
            rtime = f.readline().rstrip()
            if rtime == "":
                self.lastChecked = datetime.utcnow()
                f.write(str(self.lastChecked))
            else:
                self.lastChecked = datetime.fromisoformat(rtime)

        self.questionIDList = [
            "2d60e98a",  # 1
            "5709d2f7",  # 2
            "1adf7bf4",  # 3
            "2d5b1e85",  # 4
            "07cf4b0d",  # 5
            "1cd8ecf5",  # 6
            "302962ae",  # 7
            "4450c279",  # 8
            "6883c80c",  # 9
            "569f85fe",  # 10
            "22c8f6b6",  # 11
            "24bf24ac",  # 12
            "1ea2b378",  # t&c
        ]

    @commands.command()
    @commands.is_owner()
    async def apiStatus(self, ctx):
        pass

    @commands.command()
    @commands.is_owner()
    async def reauth(self, ctx):
        storage = file.Storage("../secrets/creds.json")
        try:
            flow = client.flow_from_clientsecrets("../secrets/client_secrets.json", self.SCOPES)
            tools.run_flow(flow, storage)
            await ctx.send("OAuth Successful")
        except:
            await ctx.send("Authentication failed")

    # get and print past responses
    @commands.command(aliases=["getr", "getR"])
    @commands.is_owner()
    async def getResponses(self, ctx, d: int = 0, h: int = 1, m: int = 0):
        service = authAPI()
        r = service.forms().responses().list(formId=self.FORM_ID,
                                             filter=f"timestamp >= {(datetime.utcnow() - timedelta(minutes=m, hours=h, days=d)).isoformat('T')}Z").execute()
        if r == {}:
            await ctx.send(f"No new responses since <t:{round((datetime.now()-timedelta(minutes=m, hours=h, days=d)).timestamp())}:R>")
            return

        c = 1
        # r['responses']['answers'][{questionId}]['textAnswers']['answers'][0]['value']
        for response in r['responses']:
            a = 1
            embed = discord.Embed(title=f"Response {c}", timestamp=datetime.utcnow(), color=0x2ecc71,
                                  # RFC-3339 Z from API -> timestamp -> unix with timezone adjustment
                                  description=f"Submitted at <t:{round((datetime.strptime(response['createTime'][:-1], '%Y-%m-%dT%H:%M:%S.%f') - timedelta(hours=4)).timestamp())}:f>")
            for ID in self.questionIDList:
                try:
                    ans = response['answers'][ID]['textAnswers']['answers'][0]['value']
                    embed.add_field(name=f"Question {a}", value=ans, inline=True)
                except KeyError:
                    embed.add_field(name=f"Question {a}", value="No Response", inline=True)
                a += 1

            await ctx.send(embed=embed)
            c += 1

    # check for new form responses every hour
    @tasks.loop(hours=1)
    async def checkFormResponses(self):
        service = authAPI()
        r = service.forms().responses().list(formId=self.FORM_ID,
                                             filter=f"timestamp >= {self.lastChecked.isoformat('T')}Z").execute()

        # rewrite file with updated lastChecked time
        with open("../secrets/lastChecked.txt", 'wt') as f:
            f.truncate()
            f.seek(0)
            f.write(str(datetime.utcnow()))

        if r == {}:
            return

        guild = self.bot.get_guild(983840745763004536)  # SOS
        notif_channel = self.bot.get_channel(994093545646456873)

        topicRoles = [
            984915844511440956,  # python
            984915918494769182,  # challenge math
            984915738798211102,  # scratch
        ]

        responseHeader = [
            "Name",  # 1
            "Grade",  # 3
            "Topic",  # 9
            "Availability",  # 10
            "Skills and Experience",  # 11
            "Requested Tutor",  # 12
        ]

        q = [0, 2, 8, 9, 10, 11]

        # r['responses']['answers'][{questionId}]['textAnswers']['answers'][0]['value']
        c = 1
        for response in r['responses']:
            msg = ""
            color = 0x2ecc71
            topic = response['answers'][self.questionIDList[8]]['textAnswers']['answers'][0]['value']
            if topic.startswith("Python"):
                msg = guild.get_role(topicRoles[0]).mention
                color = 0x2ecc71
            elif topic.startswith("Challenge Math"):
                msg = guild.get_role(topicRoles[1]).mention
                color = 0x3498db
            elif topic.startswith("Scratch"):
                msg = guild.get_role(topicRoles[2]).mention
                color = 0xe67e22
            else:
                for r in topicRoles:
                    msg += guild.get_role(r).mention
                    pass

            embed = discord.Embed(title=f"New Response {c}", timestamp=datetime.utcnow(), color=color,
                                  # RFC-3339 Z from API -> timestamp -> unix with timezone adjustment
                                  description=f"Form submitted at <t:{round((datetime.strptime(response['createTime'][:-1], '%Y-%m-%dT%H:%M:%S.%f') - timedelta(hours=4)).timestamp())}:f>")
            for i in range(len(q)):
                try:
                    ans = response['answers'][self.questionIDList[q[i]]]['textAnswers']['answers'][0]['value']
                    embed.add_field(name=f"{responseHeader[i]}", value=ans, inline=True)
                except KeyError:
                    embed.add_field(name=f"{responseHeader[i]}", value="No Response", inline=True)
            c += 1

            await notif_channel.send(f"{msg}", embed=embed)


def setup(bot):
    bot.add_cog(notification(bot))
