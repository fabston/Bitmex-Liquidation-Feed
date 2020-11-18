# ---------------------------------------------- #
# Plugin Name           : BitmexLiquidationFeed  #
# Author Name           : vsnz                   #
# File Name             : config.py              #
# ---------------------------------------------- #

liquidation_threshold = 50000      # Contract size
send_terminal_alerts  = True

# Telegram Settings
send_telegram_alerts = False
tg_token             = ''    # Bot token. Get it from @Botfather
channel              = 0     # Channel ID (ex. -1001487568087)

# Discord Settings
send_discord_alerts = False
discord_webhook     = ''     # Discord Webhook URL (https://support.discordapp.com/hc/de/articles/228383668-Webhooks-verwenden)