from xync_schema.models import Ex, Pm, Pmex


# Create Payment methods(types)
async def pt_db(pmd: dict, ex: Ex = None) -> Pm:
    df = {
        "template": pmd.get("template"),
        "logo": pmd.get("bankImage", pmd.get("bankImageWeb", None)),
        "color": pmd.get("color", None),
    }
    try:
        pm, _ = await Pm.update_or_create(df, name=pmd["name"].replace("ú", "u"))
    except ValueError as ve:
        print(pm, ve)
    if ex:  # if Ex defined: add pmex
        await Pmex.update_or_create({"exid": pmd["payMethodId"]}, ex=ex, pm=pm)
    return pm
