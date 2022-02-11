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

def giveaway(name, is_owner):
    if is_owner:
        txt = (
f"""
OWNER GIVEWAY **{name}** LAUNCHED !
"""
        )
    else:
        txt = (
f"""
GIVEWAY **{name}** LAUNCHED !
"""
        )
    return txt