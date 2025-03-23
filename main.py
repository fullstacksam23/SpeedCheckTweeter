from internet_speed_bot import InternetSpeedTwitterBot

DOWN = 100
UP = 100
bot = InternetSpeedTwitterBot(UP, DOWN)
bot.get_internet_speed()
if bot.up < UP or bot.down < DOWN:
    bot.tweet_at_provider()
    print(f"message posted: {bot.msg}")
else:
    print("Internet speeds are above the threshold. No messages were posted")
bot.driver.quit()

