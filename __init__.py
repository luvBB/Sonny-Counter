from sopel import plugin
from sopel.formatting import plain


@plugin.require_chanmsg
@plugin.rule(r"^!n\b") # only match !n at the start of a message
def count_n(bot, trigger):
    # inits the value to 0 if never counted before
    n_count = bot.db.get_nick_value(trigger.nick, "n_count", 0)

    # increment the stored value
    bot.db.set_nick_value(trigger.nick, "n_count", n_count + 1)


@plugin.require_chanmsg
@plugin.rule(r"^!nt\b") # only match !nt at the start of a message
def count_nt(bot, trigger):
    # inits the value to 0 if never counted before
    nt_count = bot.db.get_nick_value(trigger.nick, "nt_count", 0)

    # increment the stored value
    bot.db.set_nick_value(trigger.nick, "nt_count", nt_count + 1)


@plugin.command('ncount')
@plugin.example('!ncount nickname')
@plugin.require_admin
def get_n_count(bot, trigger):
    """See how many times a user has used the !n command."""
    # trigger.group(2) would be the 'nickname' in the example above'
    target = plain(trigger.group(2) or '')

    # if we don't have a target, exit
    if not target:
        return bot.reply("You need to supply a nickname.")

    # get the count. init to 0 if needed.
    n_count = bot.db.get_nick_value(target, "n_count", 0)

    # say it!
    bot.say(f"User: {target} | !n count: {n_count}")


@plugin.command('ntcount')
@plugin.example('!ntcount nickname')
@plugin.require_admin
def get_nt_count(bot, trigger):
    """See how many times a user has used the !nt command."""
    # trigger.group(2) would be the 'nickname' in the example above'
    target = plain(trigger.group(2) or '')

    # if we don't have a target, exit
    if not target:
        return bot.reply("You need to supply a nickname.")

    # get the count. init to 0 if needed.
    nt_count = bot.db.get_nick_value(target, "nt_count", 0)

    # say it!
    bot.say(f"User: {target} | !nt count: {nt_count}")


@plugin.command('ncountreset')
@plugin.require_admin
def ncount_reset(bot, trigger):
    """Use this command to wipe all stored ncount and ntcount data."""
    try:
        bot.db.execute("DELETE FROM nick_values WHERE key = 'n_count';")
        bot.db.execute("DELETE FROM nick_values WHERE key = 'nt_count';")
    except Exception:
        return bot.reply("Error purging ncount/ntcount data.")
    bot.say("All ncount/ntcount data deleted.")
