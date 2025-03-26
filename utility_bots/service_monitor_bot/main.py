import asyncio
from src.bot.discord_monitor_bot import create_bot
from src.config.settings import config

async def main():
    """
    主非同步入口函數
    負責建立和運行機器人
    """
    bot = create_bot()
    
    try:
        await bot.start(config.discord_token)
    except Exception as e:
        print(f"機器人啟動失敗: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 