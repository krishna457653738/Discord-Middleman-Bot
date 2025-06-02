# Cryptocurrency Middleman Discord Bot

- **please leave a star if you want more updates, for assistance/feature requests message @highnotes on discord**

## 🌟 Features

- **Secure Escrow System**: Automated cryptocurrency holding until deal completion 
- **Role-Based Transactions**: Clear sending/receiving role assignment 
- **Dual Confirmation**: Both parties must confirm at each step 
- **Amount Verification**: USD amount confirmation before processing 
- **Reset Functionality**: Easy transaction restart if needed
- **Timeout Protection**: Automatic timeout handling for user responses
- **Rich UI**: Beautiful Discord embeds with intuitive button interactions

## Start

### **Prerequisites**
- Python 3.8+
- Discord Bot Token
- Required Python packages (see requirements.txt)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd My_Middleman_Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   - Create a Discord application and bot at [Discord Developer Portal](https://discord.com/developers/applications)
   - Copy the bot token
   - Configure the bot token in your environment or `bot.py`

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Usage

### **Starting a Transaction**

1. **Invite the bot** to your Discord server with appropriate permissions
2. **Create a ticket/channel** where the transaction will take place
3. **Trigger the middleman service** (specific command depends on your setup)

### **Transaction Flow**

1. **Role Selection**
   - Users click "Sending" or "Receiving" buttons
   - Both roles must be filled by different users
   - Reset option available if needed

2. **Role Confirmation**
   - Both users must confirm the role assignments are correct
   - If incorrect, the process restarts with new role selection

3. **Amount Entry**
   - Sending user enters the USD amount
   - Example: `100.59` for $100.59

4. **Amount Confirmation**
   - Both users confirm the amount is correct
   - If incorrect, amount entry restarts

5. **Final Processing**
   - Bot transfers control to the LTC service
   - Cryptocurrency escrow process begins

## 🔧 Configuration

### **Environment Variables**
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### **Bot Permissions**
The bot requires the following Discord permissions:
- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands (if implemented)
- Manage Messages (for cleanup operations)

##Development

### **Adding New Cryptocurrencies**

1. **Create view classes** in `views/{crypto}/`:
   ```python
   # views/btc/role_selection_view.py
   from views.base_view import BaseMiddlemanView
   
   class RoleSelectionBTCView(BaseMiddlemanView):
       # Bitcoin-specific implementation
       pass
   ```

2. **Create the service cog**:
   ```python
   # cogs/middleman_service_btc.py
   from views.base_middleman_service import BaseMiddlemanService
   
   class MiddlemanServiceBTC(BaseMiddlemanService):
       def __init__(self, bot):
           super().__init__(bot, "Bitcoin")
       
       def _get_role_selection_view_class(self):
           return RoleSelectionBTCView
   ```

3. **Load the cog** in your bot setup

### **Customizing Embeds**

All embeds are created through the `EmbedFactory` class for consistency:

```python
from utils.embed_factory import EmbedFactory

# Create custom embeds
embed = EmbedFactory.create_role_selection_embed("Bitcoin")
embed = EmbedFactory.create_welcome_embed()
```

### **Extending Functionality**

The base classes provide hooks for extending functionality:

- **`BaseMiddlemanView`**: Common UI interactions
- **`BaseMiddlemanService`**: Service orchestration
- **`EmbedFactory`**: Consistent styling

## Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Timeout Handling**: Automatic timeout for user responses (5 minutes)
- **Error Recovery**: Graceful handling of Discord API errors
- **Role Verification**: Strict role assignment and confirmation
- **Secure Cleanup**: Automatic message cleanup after completion

## Troubleshooting

### **Common Issues**

**Bot not responding to commands:**
- Check bot permissions in the Discord server
- Verify the bot token is correct
- Ensure the bot is online and properly connected

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that Python path includes the project directory

**View buttons not working:**
- Verify Discord.py version compatibility
- Check bot permissions for message interactions
- Ensure views are properly registered

### **Debug Mode**

Enable debug logging by modifying `bot.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Requirements

See `requirements.txt` for the complete list of dependencies:
- discord.py
- asyncio (built-in)
- Additional dependencies as needed

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-crypto`
3. Make your changes following the existing architecture patterns
4. Test thoroughly
5. Submit a pull request

### **Code Style**
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all classes and methods
- Keep functions focused and modular

## 🔗 Links

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python Documentation](https://docs.python.org/3/)

## Support

If you encounter any issues or need help with setup:

1. Check the troubleshooting section above
2. Review the debug logs
3. Open an issue with detailed information about the problem

---

**⚠️ Security Notice**: This bot handles cryptocurrency transactions. Always test thoroughly in a development environment before using in production. Ensure proper security measures are in place for your Discord server and bot hosting environment. 
