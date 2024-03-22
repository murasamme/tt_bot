from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    MessageSegment,
    Message
    )

from .config import Config
from .trie import *
from .game_monitor import *
from . import _datac

__version__ = "0.1.1"
__plugin_meta__ = PluginMetadata(
    name="FGO猜从者",
    description="FGO猜从者插件，基于原HoshinoBot猜从者模块修改，感谢原作者。",
    usage="使用指令 `猜从者` 开始游戏，游戏过程中使用指令 `/quitfgo` 结束游戏。",
    config=Config,
    homepage="https://github.com/influ3nza/nonebot-plugin-fgoavatarguess",
    type="application",
    supported_adapters={"~onebot.v11"},
    # extra={"License": "MIT", "Author": "influ3nza"},
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

fgo_guess = on_command("猜从者")

trie_ = Trie_()
game_monitor = Game_monitor()


def name2id(name):
    return trie_.get_id(name)


@fgo_guess.handle()
async def handle(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    if game_monitor.game_status(group_id):
        await fgo_guess.send("此轮游戏还未结束。")
        return

    file_path = game_monitor.game_start(group_id)
    crop_path = crop_img(file_path, group_id)

    msg = Message()
    msg += MessageSegment.text("请说出以下图片出自哪位从者？")
    msg += MessageSegment.image(crop_path)
    msg += MessageSegment.text("发送/quitfgo放弃猜测。")

    await fgo_guess.send(msg)


@fgo_guess.receive()
async def receive(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    user_id = event.get_session_id().split("_")[2]

    if str(event.message).strip() == "/quitfgo":
        finmsg = "强制退出。正确答案是：" + _datac.CHARA_NAME[game_monitor.get_correct_answer(group_id)][0]
        finmsg += MessageSegment.image(game_monitor.get_correct_img(group_id))

        game_monitor.game_set(group_id)
        await fgo_guess.finish(finmsg)
        return

    if trie_.get_id(str(event.message).strip()) == game_monitor.get_correct_answer(group_id):
        d = await bot.get_group_member_info(group_id=group_id, user_id=user_id)

        finmsg = "@" + d["nickname"] + " 猜对了！正确答案是：" + _datac.CHARA_NAME[game_monitor.get_correct_answer(group_id)][0]
        finmsg += MessageSegment.image(game_monitor.get_correct_img(group_id))

        game_monitor.game_set(group_id)
        await fgo_guess.finish(finmsg)
    else:
        await fgo_guess.reject()
