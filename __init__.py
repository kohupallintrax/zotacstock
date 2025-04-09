from .zotacstock import CheckZotac


async def setup(bot):
    cog = CheckZotac(bot)
    r = bot.add_cog(cog)
    if r is not None:
        await r