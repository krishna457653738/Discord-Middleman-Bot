import discord
from discord.ext import commands
from utils.embed_factory import EmbedFactory


class BaseMiddlemanService(commands.Cog):
    """Base class for cryptocurrency middleman services."""
    
    def __init__(self, bot, crypto_name):
        self.bot = bot
        self.crypto_name = crypto_name

    async def next_step(self, channel):
        """Initialize the middleman service flow."""
        try:
            await self._send_initial_embeds(channel)
        except Exception as e:
            print(f"Error in next_step for {self.crypto_name}: {e}")

    async def _send_initial_embeds(self, channel):
        """Send the initial sequence of embeds for the middleman service."""
        # Welcome embed
        welcome_embed = EmbedFactory.create_welcome_embed()
        await channel.send(embed=welcome_embed)

        # Safety warning embed
        safety_embed = EmbedFactory.create_safety_warning_embed()
        await channel.send(embed=safety_embed)

        # Role selection embed with interactive buttons
        role_embed = EmbedFactory.create_role_selection_embed(self.crypto_name)
        message = await channel.send(embed=role_embed)

        # Attach the view to handle button interactions
        view_class = self._get_role_selection_view_class()
        view = view_class(last_embed_message=message, bot=self.bot)
        await message.edit(view=view)

    def _get_role_selection_view_class(self):
        """
        Get the appropriate role selection view class for this crypto.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _get_role_selection_view_class")

    @property
    def service_name(self):
        """Get the service name for logging and identification."""
        return f"{self.crypto_name}Service" 