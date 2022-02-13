import db_discord_helper as db

def rules():
    txt = (
"""
👉 Go to channel give-aways and type your ETH wallet address.
Example:
`0x5b5d30f1B2BF7b81214D3678aAe73D4e5F7455f5`
"""
    )
    return txt

def giveaway(is_owner):
    owner_txt = (
f"""
**OWNER GIVEWAY LAUNCHED !**
"""
        )
    general_txt = (
f"""
**GIVEWAY LAUNCHED !**
"""
        )
    return owner_txt if is_owner else general_txt

def already_giveaway(is_owner):
    already_owner_txt = (
f"""
There already is an owner giveaway ongoing. Close it before launching a new one.
"""
    )
    already_non_owner_txt = (
f"""
There already is a non owner giveaway ongoing. Close it before launching a new one.
"""
    )
    return already_owner_txt if is_owner else already_non_owner_txt

def no_ongoing_giveway():
    txt = (
"""
There is no ongoing giveaway. Come back later!
"""
    )
    return txt

def wrong_wallet_address():
    txt = (
"""
Make sure you provide a regular ETH wallet address to enter the giveaway.
Your message should **ONLY** contain the wallet adress.
Example:
`0x5b5d30f1B2BF7b81214D3678aAe73D4e5F7455f5`
"""
    )
    return txt

def channel_reserved():
    txt = (
"""
The giveaway channel is only meant to provide a wallet address during giveaways.
"""
    )
    return txt

def wallet_does_not_match(member):
    txt = (
f"""
Apparently this wallet is already claimed by {member.mention}.
If you are the real owner of this wallet, please contact {db.get_member_by_id('786520283392507925').mention} or {db.get_member_by_id('375291554543173632').mention}.
"""
    )
    return txt

def member_already_in_giveaway():
    txt = (
"""
You already registered for this giveaway(s).
"""
    )
    return txt

def successful_giveaway_register():
    txt = (
"""
Your participation was successfully registered.
"""
    )
    return txt