import discord
from discord.ui import Button
from views.base_view import BaseMiddlemanView
from utils.embed_factory import EmbedFactory
import asyncio


class ConfirmationLTCView(BaseMiddlemanView):
    """View for handling role confirmation in LTC middleman transactions."""
    
    def __init__(self, role_embed_message, sending_user, receiving_user, bot):
        super().__init__(timeout=None)
        self.role_embed_message = role_embed_message
        self.sending_user = sending_user
        self.receiving_user = receiving_user
        self.bot = bot

    @discord.ui.button(label="Correct", style=discord.ButtonStyle.success, custom_id="confirm_correct_ltc")
    async def correct_button(self, interaction: discord.Interaction, button: Button):
        required_users = [self.sending_user, self.receiving_user]
        all_confirmed = await self.handle_user_confirmation(interaction, required_users)
        
        if all_confirmed:
            await self._delete_all_after_please_read(interaction)
            await self._resend_confirmation_embed(interaction)
            await self._send_amount_request_embed(interaction.channel)

    @discord.ui.button(label="Incorrect", style=discord.ButtonStyle.danger, custom_id="confirm_incorrect_ltc")
    async def incorrect_button(self, interaction: discord.Interaction, button: Button):
        await self.role_embed_message.delete()
        await interaction.message.delete()
        await self.delete_correct_response_messages()
        await self._send_new_role_selection_embed(interaction.channel)

    async def _delete_all_after_please_read(self, interaction):
        """Delete all messages after the role embed message."""
        async for message in interaction.channel.history(after=self.role_embed_message, oldest_first=True):
            try:
                await message.delete()
            except discord.NotFound:
                # Message already deleted
                pass

    async def _resend_confirmation_embed(self, interaction):
        """Resend the confirmation embed after cleanup."""
        confirmation_embed = EmbedFactory.create_role_confirmation_embed(
            self.sending_user, 
            self.receiving_user, 
            "Litecoin"
        )
        await interaction.channel.send(embed=confirmation_embed)

    async def _send_amount_request_embed(self, channel):
        """Send embed requesting deal amount and wait for response."""
        amount_request_embed = EmbedFactory.create_amount_request_embed()
        await channel.send(content=f"{self.sending_user.mention}", embed=amount_request_embed)

        def check(m):
            return m.author == self.sending_user and m.channel == channel

        try:
            response = await self.bot.wait_for('message', check=check, timeout=300)
            amount = response.content.strip()
            await self._handle_amount_confirmation(channel, amount)
        except asyncio.TimeoutError:
            timeout_embed = await self.create_timeout_embed()
            await channel.send(embed=timeout_embed)

    async def _handle_amount_confirmation(self, channel, amount):
        """Handle the amount confirmation process."""
        amount_confirmation_embed = EmbedFactory.create_amount_confirmation_embed(amount)
        
        # Import here to avoid circular imports
        from views.ltc.amount_confirmation_view import AmountConfirmationLTCView
        view = AmountConfirmationLTCView(channel, amount, self.sending_user, self.receiving_user, self.bot)
        await channel.send(embed=amount_confirmation_embed, view=view)

    async def _send_new_role_selection_embed(self, channel):
        """Send a new role selection embed when restarting the process."""
        new_embed = EmbedFactory.create_role_selection_embed("Litecoin")
        new_message = await channel.send(embed=new_embed)
        
        # Import here to avoid circular imports
        from views.ltc.role_selection_view import RoleSelectionLTCView
        new_view = RoleSelectionLTCView(last_embed_message=new_message, bot=self.bot)
        await new_message.edit(view=new_view) 