import discord
from discord.ui import Button
from views.base_view import BaseMiddlemanView
from utils.embed_factory import EmbedFactory
import asyncio


class AmountConfirmationLTCView(BaseMiddlemanView):
    """View for handling amount confirmation in LTC middleman transactions."""
    
    def __init__(self, channel, amount, sending_user, receiving_user, bot):
        super().__init__(timeout=None)
        self.channel = channel
        self.amount = amount
        self.sending_user = sending_user
        self.receiving_user = receiving_user
        self.bot = bot

    @discord.ui.button(label="Correct", style=discord.ButtonStyle.success, custom_id="amount_correct_ltc")
    async def correct_button(self, interaction: discord.Interaction, button: Button):
        required_users = [self.sending_user, self.receiving_user]
        all_confirmed = await self.handle_user_confirmation(interaction, required_users)
        
        if all_confirmed:
            await self.delete_correct_response_messages()
            await self._call_ltc_service(interaction)

    @discord.ui.button(label="Incorrect", style=discord.ButtonStyle.danger, custom_id="amount_incorrect_ltc")
    async def incorrect_button(self, interaction: discord.Interaction, button: Button):
        await interaction.message.delete()
        await self.delete_correct_response_messages()
        await self._send_amount_request_embed(interaction.channel)

    async def _call_ltc_service(self, interaction):
        """Call the LTC service to proceed with final steps."""
        ltc_service_cog = self.bot.get_cog('LTCService')
        if ltc_service_cog:
            await ltc_service_cog.send_final_steps(
                self.channel, 
                self.amount, 
                self.sending_user, 
                self.receiving_user
            )
        else:
            print("[DEBUG] LTCService not found")
        await interaction.response.defer()

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
        view = AmountConfirmationLTCView(channel, amount, self.sending_user, self.receiving_user, self.bot)
        await channel.send(embed=amount_confirmation_embed, view=view) 