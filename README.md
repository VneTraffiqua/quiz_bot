# quiz-bot
![tg.gif](https://dvmn.org/media/filer_public/e9/eb/e9ebd8aa-17dd-4e82-9f00-aad21dc2d16c/examination_tg.gif)
![vk.gif](https://dvmn.org/media/filer_public/aa/c8/aac86f90-29b6-44bb-981e-02c8e11e69f7/examination_vk.gif)

There are three scripts in this repository, ```tg_bot.py``` bot for Telegram, ```vk_bot.py``` bot for [VK](https://vk.com), 
scripts use Redis to store user data. To connect to it, you need to get the database address, its port and password.
```questions_agregator.py``` is a script for generating questions into a ```.json``` file.

## How to install?

1. Copy the contents of the project to your working directory.

    Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

    ```
    pip install -r requirements.txt
    ```
    Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project


2. Added to `.env` file:

   `TG_TOKEN` - Telegram token. You will receive it when registering a bot

   `VK_TOKEN` - VK bot token. You can get it in your community settings

    `REDIS_HOST` -  Host address of your Redis database server

    `REDIS_PORT` - Port number of the Redis database server

    `REDIS_PASS` - Password to connect to the Redis database

## Launch.

Launch telegram bot:

```
python3 tg_bot.py
```

Launch VK bot:
```
python3 vk_bot.py