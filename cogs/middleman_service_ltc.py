import discord
from discord.ext import commands
from views.base_middleman_service import BaseMiddlemanService
from views.ltc.role_selection_view import RoleSelectionLTCView


class MiddlemanServiceLTC(BaseMiddlemanService):
    """Cog for handling Litecoin middleman transactions."""
    
    def __init__(self, bot):
        super().__init__(bot, "Litecoin")

    def _get_role_selection_view_class(self):
        """Get the LTC role selection view class."""
        return RoleSelectionLTCView


async def setup(bot):
    """Setup function for loading the cog."""
    await bot.add_cog(MiddlemanServiceLTC(bot))
