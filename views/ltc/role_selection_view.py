import discord
from discord.ui import Button
from views.base_view import BaseMiddlemanView
from utils.embed_factory import EmbedFactory


class RoleSelectionLTCView(BaseMiddlemanView):
    """View for handling role selection in LTC middleman transactions."""
    
    def __init__(self, last_embed_message, bot):
        super().__init__(timeout=None)
        self.last_embed_message = last_embed_message
        self.sending_user = None
        self.receiving_user = None
        self.bot = bot

    @discord.ui.button(label="Sending", style=discord.ButtonStyle.primary, custom_id="role_sending_ltc")
    async def sending_button(self, interaction: discord.Interaction, button: Button):
        await self._handle_role_selection(interaction, "sending")

    @discord.ui.button(label="Receiving", style=discord.ButtonStyle.success, custom_id="role_receiving_ltc")
    async def receiving_button(self, interaction: discord.Interaction, button: Button):
        await self._handle_role_selection(interaction, "receiving")

    @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger, custom_id="role_reset_ltc")
    async def reset_button(self, interaction: discord.Interaction, button: Button):
        self.sending_user = None
        self.receiving_user = None
        await self._update_embed()
        await interaction.response.defer()

    async def _handle_role_selection(self, interaction, role):
        """Handle user selecting a role."""
        if role == "sending":
            if self.sending_user or interaction.user == self.receiving_user:
                await interaction.response.defer()
                return
            self.sending_user = interaction.user
        else:  # receiving
            if self.receiving_user or interaction.user == self.sending_user:
                await interaction.response.defer()
                return
            self.receiving_user = interaction.user
        
        await self._update_embed()
        await interaction.response.defer()
        await self._check_roles_complete()

    async def _update_embed(self):
        """Update the embed with current role assignments."""
        embed = self.last_embed_message.embeds[0]
        embed.set_field_at(
            0, 
            name="Sending Litecoin", 
            value=self.sending_user.mention if self.sending_user else "`None`", 
            inline=True
        )
        embed.set_field_at(
            1, 
            name="Receiving Litecoin", 
            value=self.receiving_user.mention if self.receiving_user else "`None`", 
            inline=True
        )
        await self.last_embed_message.edit(embed=embed)

    async def _check_roles_complete(self):
        """Check if both roles are filled and proceed to confirmation."""
        if self.sending_user and self.receiving_user:
            confirmation_embed = EmbedFactory.create_role_confirmation_embed(
                self.sending_user, 
                self.receiving_user, 
                "Litecoin"
            )
            
            await self._disable_buttons()
            
            # Import here to avoid circular imports
            from views.ltc.confirmation_view import ConfirmationLTCView
            view = ConfirmationLTCView(
                self.last_embed_message, 
                self.sending_user, 
                self.receiving_user, 
                self.bot
            )
            await self.last_embed_message.channel.send(embed=confirmation_embed, view=view)

    async def _disable_buttons(self):
        """Disable all buttons in the view."""
        for item in self.children:
            item.disabled = True
        await self.last_embed_message.edit(view=self) 