from aadiscordbot.app_settings import get_site_url
from aadiscordbot.cogs.utils.decorators import sender_has_perm
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands

from django.conf import settings

from allianceauth.services.hooks import get_extension_logger

from evescout.models import SignaturePinger

logger = get_extension_logger(__name__)


class EveScout(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    evescout_commands = SlashCommandGroup(
        "evescout", "EVE-Scouts", guild_ids=[int(settings.DISCORD_GUILD_ID)]
    )

    @evescout_commands.command(
        name="initiate-pinger",
        description="Initiate the configuration for pings when a Thera/Turnur connection is reported",
    )
    @sender_has_perm("evescout.create_pinger")
    async def initiate_pinger(self, ctx: ApplicationContext):
        """Creates a new pinger and link it to the channel the command was called in"""
        channel_id = ctx.channel_id
        logger.info("Creating a pinger for channel id %s", channel_id)

        pinger = SignaturePinger.create(channel_id)

        site_url = get_site_url()
        pinger_url = f"{site_url}/admin/evescout/signaturepinger/{pinger.id}"

        return await ctx.respond(
            f"Successfully created a new pinger. You can edit it at {pinger_url}"
        )


def setup(bot):
    bot.add_cog(EveScout(bot))
