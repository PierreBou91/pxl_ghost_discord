def rules():
    txt = (
"""
👉 Go to channel give-aways and type : /giv <your wallet adress> 
        example: `/giv 0x0652837479284478393940038848`

If you already are an owner:
👉 Go to channel haunted-tavern  and type : /own <your wallet adress>
        example: `/own 0x0652837479284478393940038848`
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