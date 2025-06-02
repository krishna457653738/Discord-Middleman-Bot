import discord


class EmbedFactory:
    """Factory class for creating common Discord embeds."""
    
    # Common colors
    SUCCESS_COLOR = 3667300
    WARNING_COLOR = 15975211
    ERROR_COLOR = 15608876
    
    @staticmethod
    def create_welcome_embed():
        """Create the initial welcome embed for middleman service."""
        embed = discord.Embed(
            title="Cryptocurrency Middleman System",
            description=(
                "> Welcome to our automated cryptocurrency Middleman system! "
                "Your cryptocurrency will be stored securely till the deal is completed.\n"
                "> The system ensures the security of both users, by securely storing "
                "the funds until the deal is complete and confirmed by both parties."
            ),
            color=EmbedFactory.SUCCESS_COLOR
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1153826027714379866/1157874378344779886/crypto.png?ex=669a7f4c&is=66992dcc&hm=9030faeb2ef0783a104d2f49a25a32408b97cda0a37a97dad91416475c177e23&"
        )
        return embed
    
    @staticmethod
    def create_safety_warning_embed():
        """Create the safety warning embed."""
        embed = discord.Embed(
            description=(
                "**Please ensure all conversations related to the deal are done within "
                "this ticket. Failure to do so may put you at risk of being scammed.**\n\n"
                "<a:Alert:1263604204216389746> **Our bot will NEVER dm you! "
                "Please report any suspicious DMs to Staff.**"
            ),
            color=EmbedFactory.ERROR_COLOR
        )
        embed.set_author(
            name="Please Read!",
            icon_url="https://cdn.discordapp.com/attachments/1153826027714379866/1187997184688398366/790938.png?ex=669aa8d8&is=66995758&hm=811186eaa7808f66177494f07a921d588ab5e612ab007cc89f8c44a0e2f7d809&"
        )
        return embed
    
    @staticmethod
    def create_role_selection_embed(crypto_name="Litecoin"):
        """Create the role selection embed."""
        embed = discord.Embed(
            title="Role Selection",
            description=(
                "Please select one of the following buttons that corresponds to your "
                "role in this deal. Once selected, both users must confirm to proceed."
            ),
            color=EmbedFactory.SUCCESS_COLOR
        )
        embed.add_field(name=f"Sending {crypto_name}", value="`None`", inline=True)
        embed.add_field(name=f"Receiving {crypto_name}", value="`None`", inline=True)
        return embed
    
    @staticmethod
    def create_role_confirmation_embed(sending_user, receiving_user, crypto_name="Litecoin"):
        """Create the role confirmation embed."""
        embed = discord.Embed(
            title="Confirmed Role Identities",
            description="Both users have confirmed their roles within this deal.",
            color=EmbedFactory.SUCCESS_COLOR
        )
        embed.add_field(name=f"Sending {crypto_name}", value=sending_user.mention, inline=True)
        embed.add_field(name=f"Receiving {crypto_name}", value=receiving_user.mention, inline=True)
        return embed
    
    @staticmethod
    def create_amount_request_embed():
        """Create the amount request embed."""
        embed = discord.Embed(
            title="Deal Amount",
            description="Please state the amount we are expected to receive in USD. (eg. 100.59)",
            color=EmbedFactory.SUCCESS_COLOR
        )
        return embed
    
    @staticmethod
    def create_amount_confirmation_embed(amount):
        """Create the amount confirmation embed."""
        embed = discord.Embed(
            title="Amount Confirmation",
            description=f"Are we expected to receive {amount} USD?",
            color=EmbedFactory.WARNING_COLOR
        )
        return embed
    
    @staticmethod
    def create_user_response_embed(user):
        """Create a user response confirmation embed."""
        embed = discord.Embed(
            description=f"{user.mention} has responded with **'Correct'**",
            color=EmbedFactory.SUCCESS_COLOR
        )
        return embed
    
    @staticmethod
    def create_timeout_embed():
        """Create a timeout embed."""
        embed = discord.Embed(
            description="You have run out of time!",
            color=EmbedFactory.ERROR_COLOR
        )
        return embed 