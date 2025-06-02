import discord
from discord.ui import View
from abc import ABC, abstractmethod
from utils.embed_factory import EmbedFactory


class BaseMiddlemanView(View, ABC):
    """Base class for all middleman service views with common functionality."""
    
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)
        self.correct_responses = set()
        self.correct_response_messages = []

    async def send_correct_response_message(self, interaction):
        """Send a response message when user clicks correct button."""
        response_embed = EmbedFactory.create_user_response_embed(interaction.user)
        response_message = await interaction.channel.send(embed=response_embed)
        self.correct_response_messages.append(response_message)
        return response_message

    async def delete_correct_response_messages(self):
        """Delete all correct response messages."""
        for msg in self.correct_response_messages:
            try:
                await msg.delete()
            except discord.NotFound:
                # Message already deleted
                pass

    async def handle_user_confirmation(self, interaction, required_users):
        """Handle user confirmation logic common to multiple views."""
        if interaction.user.id in self.correct_responses:
            await interaction.response.send_message("You have already confirmed.", ephemeral=True)
            return False

        self.correct_responses.add(interaction.user.id)
        await self.send_correct_response_message(interaction)

        # Check if all required users have confirmed
        all_confirmed = all(user.id in self.correct_responses for user in required_users)
        
        if not all_confirmed:
            await interaction.response.defer()
        
        return all_confirmed

    @staticmethod
    async def create_timeout_embed():
        """Create a timeout embed."""
        return EmbedFactory.create_timeout_embed() 