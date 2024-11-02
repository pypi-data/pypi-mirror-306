from xync_client.Binance.sapi import Sapi
from xync_client.Binance.web import Public
from xync_client.Htx.web import Public as Htx
from pg_channel import plsql
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from uvloop import run
from xync_schema import models
from xync_schema.models import Ex, Pm, Cur, Pmcur, Country, Coin, Pmex, ExType, PmType, Curex, TestEx, ExAction

from xync_script.utils import pt_db
from xync_script.loader import BKEY, BSEC, dsn


async def main():
    cn = await init_db(dsn, models, True)

    exs = {
        "Beribit": (
            ExType.p2p,
            "https://sun9-41.userapi.com/impg/cZCGFTXH5-11_HjiWw9aWr3__SlbmMIiXSc-ig/YtOHJpjuVW0.jpg?size=604x604&quality=95&sign=def93bbe4283c563eb2d75a5968350f2",
            "beribit.app",
            "beribit.app",
            "beribit.app/login",
        ),
        "Binance": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/52/large/binance.jpg",
            "binance.com",
            "binance.com",
            "accounts.binance.com/login",
        ),
        "BingX": (
            ExType.p2p,
            "https://assets.coingecko.com/markets/images/812/large/YtFwQwJr_400x400.jpg",
            "bingx.com",
            "bingx.com",
            "bingx.com/login",
        ),
        "Bisq": (ExType.p2p, "", "", "", ""),
        "BitcoinGlobal": (ExType.p2p, "", "", "", ""),
        "BitGet": (
            ExType.p2p,
            "https://assets.coingecko.com/markets/images/591/large/2023-07-25_21.47.43.jpg",
            "www.bitget.com",
            "www.bitget.com",
            "www.bitget.com/login",
        ),
        "BitPapa": (
            ExType.p2p,
            "https://avatars.mds.yandex.net/i?id=130c32d9900d514d738ef89b9c61bcd3_l-4767909-images-thumbs&n=13",
            "bitpapa.com",
            "bitpapa.com",
            "bitpapa.com/log-in",
        ),
        "Bitvalve ": (ExType.p2p, "", "", "", ""),
        "Bybit": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/698/large/bybit_spot.png",
            "bybit.com",
            "bybit.com",
            "bybit.com/login",
        ),
        "CoinCola": (ExType.main, "", "", "", ""),
        "CRYPTED": (ExType.p2p, "", "", "", ""),
        "Garantex": (ExType.p2p, "", "", "", ""),
        "Gate": (
            ExType.p2p,
            "https://assets.coingecko.com/markets/images/403/large/gate_io_logo.jpg",
            "gate.io",
            "gate.io",
            "www.gate.io/login",
        ),
        "HodlHodl": (ExType.p2p, "", "", "", ""),
        "Htx": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/25/large/logo_V_colour_black.png",
            "www.htx.com",
            "www.htx.com",
            "htx.com/login",
        ),
        "Koshelek": (ExType.p2p, "", "", "", ""),
        "KuCoin": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/61/large/kucoin.png",
            "kucoin.com",
            "kucoin.com",
            "www.kucoin.com/ucenter/signin",
        ),
        "LocalCoinSwap": (ExType.p2p, "", "", "", ""),
        "LocalMonero": (ExType.p2p, "", "", "", ""),
        "Mexc": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/409/large/MEXC_logo_square.jpeg",
            "www.mexc.com",
            "www.mexc.com",
            "www.mexc.com/login",
        ),
        "Noones ": (ExType.p2p, "", "", "", ""),
        "Okx": (
            ExType.main,
            "https://assets.coingecko.com/markets/images/379/large/WeChat_Image_20220117220452.png",
            "www.okx.cab",
            "www.okx.cab",
            "www.okx.cab/account/login",
        ),
        "Paxful": (ExType.p2p, "", "", "", ""),
        "PeachBitcoin": (ExType.p2p, "", "", "", ""),
        "Phemex": (ExType.p2p, "", "", "", ""),
        "Poloniex": (ExType.main, "", "", "", ""),
        "Remitano": (ExType.p2p, "", "", "", ""),
        "RiseX": (ExType.p2p, "", "", "", ""),
        "RoboSats": (ExType.p2p, "", "", "", ""),
        "Sigen": (
            ExType.p2p,
            "https://yastatic.net/naydex/yandex-search/neZ1W6346/a21f02dA/2SvJ6dTLJwRiz_lTFP-fhywHqi1fxPNRcIxuKzcpwJ0DGlJzbzdT8ARet86SrINoGNj87R9U-t8HLZcrrBASQf0_6OkAL7cgl6uc0gCrHxI9Y369emE2MJF5yotCyODdZ5iXljtkQJMXTMV9VXsEL68seaiqQF578wnB3V",
            "sigen.pro",
            "sigen.pro",
            "sigen.pro/p2p",
        ),
        "SkyCrypto": (ExType.p2p, "", "", "", ""),
        "SmartSwap": (ExType.p2p, "", "", "", ""),
        "Solid": (ExType.main, "", "", "", ""),
        "TgWallet": (
            ExType.p2p,
            "https://telerock.ru/uploads/posts/2024-03/f658443d9e_c9d505bbf856e2360ba6812079ba02d0.webp",
            "walletbot.me",
            "p2p.walletbot.me",
            "walletbot.me",
        ),
        "TotalCoin": (ExType.p2p, "", "", "", ""),
        "WazirX": (ExType.p2p, "", "", "", ""),
        "WebMoney": (
            ExType.p2p,
            "https://vectorseek.com/wp-content/uploads/2023/08/Webmoney-Icon-Logo-Vector.svg-.png",
            "exchanger.money",
            "exchanger.money",
            "exchanger.money",
        ),
        "WhiteBIT": (ExType.p2p, "", "", "", ""),
        "xRocket": (
            ExType.p2p,
            "https://cdn.allmylinks.com/prod/Upload/file/R/L/6/8G0TaGNtUV8C1V7VQsivDtJcpEz2z7Lc.jpg",
            "",
            "",
            "",
        ),
        # "catalogop2p(.com": ExType.p2p, ''), todo: discover brazilian p2p platforms
    }
    await Ex.bulk_create(
        (
            Ex(name=n, type_=val[0], logo=val[1], host=val[2], host_p2p=val[3], url_login=val[4])
            for n, val in exs.items()
        ),
        update_fields=["host", "host_p2p", "logo", "url_login"],
        on_conflict=["name", "type_"],
    )
    texs = [TestEx(ex=ex, action=act) for act in ExAction for ex in await Ex.exclude(logo="")]
    await TestEx.bulk_create(texs, ignore_conflicts=True)

    htx = await Ex.get(name="Htx")
    bex = await Ex.get(name="Binance")

    async def htx_init():
        # # # Get data from HUOBI
        hwp = Htx(htx.host)
        countries, pay_methods, currencies, coins = await hwp.get_all()
        await hwp.close()

        pms: {int: Pm} = {pm["payMethodId"]: await pt_db(pm, htx) for pm in pay_methods}

        # # Currency prepare
        for c in currencies:
            if c["currencyId"] == 172:
                c["currencyId"] = 1
        await Cur.get_or_create(id=25, ticker="MMK")
        await Cur.get_or_create(id=8, ticker="KRW")
        currencies = sorted(currencies, key=lambda x: x["nameShort"])
        # and create
        cc: {str: Cur} = {
            c["nameShort"]: (await Cur.get_or_create({"id": c["currencyId"]}, ticker=c["nameShort"]))[0]
            for c in currencies
        }
        # with curex
        curexs = [Curex(cur=c, ex=htx) for c in cc.values()]
        await Curex.bulk_create(curexs, ignore_conflicts=True)

        # # Link PayMethods with currencies
        wrong_pt_ids = (4, 498, 14, 15, 16, 34, 20009, 20010)  # these ids not exist in pms
        ptcs_in_curs = [
            [
                {"cur": cc[c["nameShort"]], "pm": pms[pm_id]}
                for pm_id in c["supportPayments"]
                if pm_id not in wrong_pt_ids
            ]
            for c in currencies
            if c["supportPayments"]
        ]
        for pmcurs in ptcs_in_curs:
            for pmcur in pmcurs:
                pmc: Pmcur = (await Pmcur.update_or_create(**pmcur))[
                    0
                ]  # ignore_conflicts because of Huobi bug: pm duplicates
                # add these paymentMethods-currencies to Huobi
                await htx.pmcurs.add(pmc)

        # Country preparing
        countries = sorted(
            (c for c in countries if c["code"] not in (999, 9999, 441624, 999999)), key=lambda x: x["name"]
        )  # sort and filter
        cnts = {
            "BosniaandHerzegovina": "BA",
            "Brunei": "BN",
            "Congo": "CD",
            "Djibouti": "DJ",
            "Guinea": "GN",
            "Iraq": "IQ",
            "Kyrgyzstan": "KG",
            "ComorosIslands": "KM",
            "Liberia": "LR",
            "Libya": "LY",
            "Yemen": "YE",
            "Zimbabwe": "ZW",
            "United States of America": "US",
            "Lebanon": "LB",
            "Central African Republic": "XA",
            "Laos": "LA",
            "Tanzania": "TZ",
            "Bangladesh": "BD",
        }
        for c in countries:  # add missed shortNames
            if cd := cnts.get(c["name"]):
                c["appShort"] = cd
        # Countries create
        cntr: [Country] = [
            Country(id=c["countryId"], cur_id=c["currencyId"], code=c["code"], name=c["name"], short=c["appShort"])
            for c in countries
        ]  # if c['currencyId'] in [cur.id for cur in await Cur.all()]
        await Country.bulk_create(cntr, ignore_conflicts=True)
        # todo: curexcountry

        # Create coins
        coins: [Coin] = [
            Coin(id=c["coinId"], is_fiat=c["coinType"] == 1, ticker=c["coinCode"], name=c["enFullName"]) for c in coins
        ]
        await Coin.bulk_create(coins, ignore_conflicts=True)

        print("Huobi DONE")

    await htx_init()

    # # # BINANCE
    async def binance_init():
        # sapi = Sapi(*(await User[0]).agents[0].auth.values())
        sapi = Sapi(BKEY, BSEC)
        # # PayMethods
        # get from api
        pms_new: [dict] = await sapi.get_pay_meths()
        # prepare old Huobi payMeths
        pms_old: {str: Pm} = {pm.name.lower().replace(" ", "").replace("-", ""): pm for pm in await Pm.all()}
        rd = {
            669: 19,
            495: 544,
            408: 67,
            185: 219,
            847: 39,
            601: 71,
            590: 38,
            443: 68,
            571: 43,
        }  # yandex, qnb, aba, millenium, touch-n-go, uala, viettel(pay/money), wing(money/combodia), (transfer)wise
        # merge with new Binance payMeths
        for pm_new in pms_new["data"]:
            name: str = pm_new["name"].lower().replace(" ", "").replace("-", "")
            idf: str = pm_new["identifier"].lower()
            typ = PmType[pm_new["typeCode"].replace("-", "_")]
            df = {
                "identifier": pm_new["identifier"],
                "type_": typ,
                "logo": pm_new["iconUrlColor"],
                "color": pm_new["bgColor"],
                "riskLevel": pm_new["riskLevel"],
                "multiAllow": pm_new["multiAllow"],
                "chatNeed": pm_new["chatNeed"],
            }
            if idf in pms_old.keys():
                pmo = pms_old.get(name, pms_old.get(idf))
            elif hid := rd.get(pm_new["id"]):
                pmo = (await Pmex.get(exid=hid, ex=htx).prefetch_related("pm")).pm
            else:
                pmo, _ = await Pm.get_or_create(df, name=pm_new["name"])
            await pmo.update_from_dict(df).save()
            # add pmex
            pmex, _ = await Pmex.update_or_create({"exid": pm_new["id"]}, ex=bex, pm=pmo)

        # # Currency
        curs = await sapi.get_fiats()
        cnt_names = {"SD": "Sudan", "XO": "West Africa", "EU": "Europe"}
        papi = Public("p2p.binance.com")
        for cur in curs["data"]:
            c: Cur = await Cur.get_or_create_by_name(cur["currencyCode"])
            curex, _ = await Curex.get_or_create(cur=c, ex=bex)  # add currency to Binance
            cnt = await Country.get_or_create_by_name(
                cur["countryCode"], "short", {"cur": c, "name": cnt_names.get(cur["countryCode"])}
            )
            # updates wrong huobi data
            if cnt.cur_id != c.id:  # wrong cur (usually USD)
                await cnt.update_from_dict({"cur": c}).save()
            # update main country name for new currencies
            await c.update_from_dict({"country": cnt.name or cnt.short or cur["countryCode"]}).save()
            pmcountries = await papi.get_pms_and_country_for_cur(cur["currencyCode"])
            # curex
            await Curex.get_or_create(cur=c, ex=bex)
            # pmcur
            for idf, idd, name in pmcountries[0]:
                if not await Pm.get_or_none(identifier=idf):
                    pmo = await Pm.get_or_none(name=name) or await Pm.get_or_none(identifier=idf)
                    if not pmo:
                        if name == "Cash":  # todo: dirty hardcode fix
                            pmo = await Pm.create(name="Cash", type_=PmType.cash)
                        else:
                            print("Pm:", name, "WHAT type?!")
                            continue
                    await pmo.update_from_dict({"identifier": idf}).save()
                    await Pmex.update_or_create({"exid": idd}, ex=bex, pm=pmo)
            pms = []
            for pm in pmcountries[0]:
                pm_ = await Pm.get_or_none(identifier=pm[0])
                if not pm_:
                    print("PM not found:", pm[0], cur["symbol"])
                else:
                    pms.append(pm_)
            await c.pms.add(*pms)
            # pmcurex
            pmcurs = await Pmcur.filter(cur=c)
            await bex.pmcurs.add(*pmcurs)
            # curex
            curex: Curex = await Curex.get(cur=c, ex=bex)
            # curexcountry
            countries = [
                await Country.get_or_create_by_name(name=cont, attr_name="short", def_dict={"cur": c})
                for cont in pmcountries[1]
            ]
            # [await cont.update_from_dict({'cur': c}).save() for cont in countries]  # no need?
            await curex.countries.add(*countries)
        await papi.close()

        # # Coins
        coins = await sapi.get_coins()
        cns = []
        for coin in coins["data"]:
            cns.append(await Coin.get_or_create_by_name(coin["asset"], "ticker"))
        await bex.coins.add(*cns)

        await sapi.close()

    await binance_init()
    print("Binance DONE")
    # await ptg()
    # print("PTG DONE")
    await pt_ranking()
    print("PM ranking DONE")
    await set_triggers(cn)
    print("triggers DONE")
    await cn.close()


async def pt_ranking():
    await Pm.filter(name__in=["Payeer"]).update(rank=-3)
    await Pm.filter(name__in=["Advcash"]).update(rank=-2)
    await Pm.filter(name__in=["RUBfiatbalance"]).update(rank=-1)
    await Pm.filter(name__in=["TinkoffNew", "DenizBank"]).update(rank=4)
    await Pm.filter(name__in=["RosBankNew", "BanktransferTurkey"]).update(rank=3)
    await Pm.filter(name__in=["RaiffeisenBank"]).update(rank=2)
    await Pm.filter(name__in=["QIWI"]).update(rank=5)
    await Pm.filter(name__in=["YandexMoneyNew"]).update(rank=6)


async def ptg():
    # todo pmex, pmcur, pmcurex
    bnr = "BinanceP2P"
    await (
        (await Pm.get_or_create({"name": "RUBfiatbalance"}, identifier="RUBfiatbalance"))[0]
        .update_from_dict({"group": bnr})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "BinanceGiftCardRUB"}, identifier="BinanceGiftCardRUB"))[0]
        .update_from_dict({"group": bnr})
        .save()
    )

    rb = "RussianBanks"
    await (
        (await Pm.get_or_create({"name": "RosBankNew"}, identifier="RosBankNew"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "TinkoffNew"}, identifier="TinkoffNew"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "PostBankNew"}, identifier="PostBankNew"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "UralsibBank"}, identifier="UralsibBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "HomeCreditBank"}, identifier="HomeCreditBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (await Pm.get_or_create({"name": "MTSBank"}, identifier="MTSBank"))[0].update_from_dict({"group": rb}).save()
    await (
        (await Pm.get_or_create({"name": "AkBarsBank"}, identifier="AkBarsBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "UniCreditRussia"}, identifier="UniCreditRussia"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "OTPBankRussia"}, identifier="OTPBankRussia"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "RussianStandardBank"}, identifier="RussianStandardBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (await Pm.get_or_create({"name": "BCSBank"}, identifier="BCSBank"))[0].update_from_dict({"group": rb}).save()
    await (
        (await Pm.get_or_create({"name": "BankSaintPetersburg"}, identifier="BankSaintPetersburg"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "CitibankRussia"}, identifier="CitibankRussia"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "CreditEuropeBank"}, identifier="CreditEuropeBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "RenaissanceCredit"}, identifier="RenaissanceCredit"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (await Pm.get_or_create({"name": "ABank"}, identifier="ABank"))[0].update_from_dict({"group": rb}).save()
    await (
        (await Pm.get_or_create({"name": "CitibankRussia"}, identifier="CitibankRussia"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "RaiffeisenBank"}, identifier="RaiffeisenBank"))[0]
        .update_from_dict({"group": rb})
        .save()
    )
    b, _ = await Pm.get_or_create({"name": "BANK"}, identifier="BANK")  # BankTransfer (only for THB)
    rub = await Cur.get(ticker="RUB")
    bp, _ = await Pmcur.get_or_create(pm=b, cur=rub)
    bp.blocked = True
    await bp.save()

    sbp, _ = await Pm.get_or_create({"name": "SBP", "rank": -5, "group": rb}, identifier="SBP")
    await Pmcur.get_or_create({"blocked": True}, pm=sbp, cur=rub)
    sbr, _ = await Pm.get_or_create({"identifier": "Sberbank", "rank": -5, "group": rb}, name="Sberbank")
    await Pmcur.get_or_create({"blocked": True}, pm=sbr, cur=rub)
    vtb, _ = await Pm.get_or_create({"name": "VTBBank", "rank": -5, "group": rb}, identifier="VTBBank")
    await Pmcur.get_or_create({"blocked": True}, pm=vtb, cur=rub)
    otkr, _ = await Pm.get_or_create({"name": "OtkritieBank", "rank": -5, "group": rb}, identifier="OtkritieBank")
    await Pmcur.get_or_create({"blocked": True}, pm=otkr, cur=rub)
    svk, _ = await Pm.get_or_create({"name": "SovkomBank", "rank": -5, "group": rb}, identifier="SovkomBank")
    await Pmcur.get_or_create({"blocked": True}, pm=svk, cur=rub)
    alf, _ = await Pm.get_or_create({"name": "AlfaBank", "rank": -5, "group": rb}, identifier="AlfaBank")
    await Pmcur.get_or_create({"blocked": True}, pm=alf, cur=rub)
    cd, _ = await Pm.get_or_create({"name": "CashDeposit", "rank": -5, "group": rb}, identifier="CashDeposit")
    await Pmcur.get_or_create({"blocked": True}, pm=cd, cur=rub)
    cip, _ = await Pm.get_or_create({"name": "CashInPerson"}, identifier="CashInPerson")
    await (await Pmcur.update_or_create(pm=cip, cur=rub))[0].update_from_dict({"blocked": True})
    sb, _ = await Pm.get_or_create(identifier="SpecificBank")
    await (await Pmcur.update_or_create(pm=sb, cur=rub))[0].update_from_dict({"blocked": True})
    ab, _ = await Pm.get_or_create({"rank": -5, "group": rb}, identifier="ABank")
    await Pmcur.get_or_create({"blocked": True}, pm=ab, cur=rub)
    kp, _ = await Pm.get_or_create(identifier="KoronaPay")
    tl, _ = await Cur.get_or_create(ticker="TRY")
    await Pmcur.get_or_create(pm=kp, cur=tl)  # hack for old orders

    tb = "TurkBanks"
    await (await Pm.get_or_create({}, identifier="Akbank"))[0].update_from_dict({"group": tb}).save()
    await (await Pm.get_or_create({"name": "Akbank"}, identifier="alBaraka"))[0].update_from_dict({"group": tb}).save()
    await (
        (await Pm.get_or_create({"name": "alBaraka"}, identifier="SpecificBank"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "SpecificBank"}, identifier="HALKBANK"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "HALKBANK"}, identifier="Fibabanka"))[0].update_from_dict({"group": tb}).save()
    )
    await (await Pm.get_or_create({"name": "Fibabanka"}, identifier="Ziraat"))[0].update_from_dict({"group": tb}).save()
    await (await Pm.get_or_create({"name": "Ziraat"}, identifier="BAKAIBANK"))[0].update_from_dict({"group": tb}).save()
    await (
        (await Pm.get_or_create({"name": "BAKAIBANK"}, identifier="Fibabanka"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "Fibabanka"}, identifier="KuveytTurk"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "KuveytTurk"}, identifier="BanktransferTurkey"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (
        (await Pm.get_or_create({"name": "BanktransferTurkey"}, identifier="VakifBank"))[0]
        .update_from_dict({"group": tb})
        .save()
    )
    await (await Pm.get_or_create({"name": "VakifBank"}, identifier="Papara"))[0].update_from_dict({"group": tb}).save()
    await (await Pm.get_or_create({"name": "Papara"}, identifier="QNB"))[0].update_from_dict({"group": tb}).save()
    await (await Pm.get_or_create({"name": "QNB"}, identifier="ISBANK"))[0].update_from_dict({"group": tb}).save()
    await (await Pm.get_or_create({"name": "ISBANK"}, identifier="Garanti"))[0].update_from_dict({"group": tb}).save()
    await (
        (await Pm.get_or_create({"name": "Garanti"}, identifier="DenizBank"))[0].update_from_dict({"group": tb}).save()
    )
    await Pmcur.get_or_create({"blocked": True}, pm=b, cur=tl)  # multi cur

    #
    eb = "EuroBanks"
    await (await Pm.get(identifier="SEPA")).update_from_dict({"group": eb}).save()
    await (await Pm.get(identifier="SEPAinstant")).update_from_dict({"group": eb}).save()
    await (await Pm.get(identifier="ING")).update_from_dict({"group": eb}).save()

    ub = "UkrBanks"
    await (await Pm.get(identifier="RaiffeisenBankAval")).update_from_dict({"group": ub}).save()


# async def fiats_init():
#     fiats = [
#         {'pmcur': Pmcur.get(cur=await Cur.get_or_create_by_name('RUB')), 'pm': Pm},
#     ]


async def set_triggers(cn: AsyncpgDBClient):
    plsql("dep", {})
    await cn.execute_script("""
CREATE OR REPLACE FUNCTION dep_upd() returns trigger as
$dep_upd_trg$
BEGIN
    IF OLD.apr!=NEW.apr OR OLD.max_limit!=NEW.max_limit THEN -- AND OLD.is_active=NEW.is_active AND OLD.fee=NEW.fee AND OLD.max_limit=NEW.max_limit AND OLD.apr_is_fixed=NEW.apr_is_fixed AND OLD.duration=NEW.duration AND OLD.early_redeem=NEW.early_redeem AND OLD.bonus_coin_id=NEW.bonus_coin_id
        PERFORM pg_notify('deps_upd', row_to_json(NEW)::varchar);
    END IF;
    RETURN NULL;
END
$dep_upd_trg$ LANGUAGE plpgsql;
CREATE TRIGGER dep_upd AFTER UPDATE ON dep FOR EACH ROW EXECUTE FUNCTION dep_upd();

CREATE OR REPLACE FUNCTION dep_new() returns trigger as
$dep_new_trg$
BEGIN
    PERFORM pg_notify('deps_new', row_to_json(NEW)::varchar);
    RETURN NULL;
END
$dep_new_trg$ LANGUAGE plpgsql;
CREATE TRIGGER dep_new AFTER INSERT ON dep FOR EACH ROW EXECUTE FUNCTION dep_new();

CREATE OR REPLACE FUNCTION dep_del() returns trigger as
$dep_del_trg$
BEGIN
    PERFORM pg_notify('deps_del', OLD.id::varchar);
    RETURN NULL;
END
$dep_del_trg$ LANGUAGE plpgsql;
CREATE TRIGGER dep_del AFTER DELETE ON dep FOR EACH ROW EXECUTE FUNCTION dep_del();


CREATE OR REPLACE FUNCTION ad_upd() returns trigger as
$ad_upd_trg$
BEGIN
    IF OLD.price!=NEW.price OR OLD.minFiat!=NEW.minFiat OR OLD.maxFiat!=NEW.maxFiat THEN
        PERFORM pg_notify('ads_upd', row_to_json(NEW)::varchar);
    END IF;
    RETURN NULL;
END
$ad_upd_trg$ LANGUAGE plpgsql;
CREATE TRIGGER ad_upd AFTER UPDATE ON ad FOR EACH ROW EXECUTE FUNCTION ad_upd();

CREATE OR REPLACE FUNCTION ad_new() returns trigger as
$ad_new_trg$
BEGIN
    PERFORM pg_notify('ads_new', row_to_json(NEW)::varchar);
    RETURN NULL;
END
$ad_new_trg$ LANGUAGE plpgsql;
CREATE TRIGGER ad_new AFTER INSERT ON ad FOR EACH ROW EXECUTE FUNCTION ad_new();

CREATE OR REPLACE FUNCTION ad_del() returns trigger as
$ad_del_trg$
BEGIN
    PERFORM pg_notify('ads_del', OLD.id::varchar);
    RETURN NULL;
END
$ad_del_trg$ LANGUAGE plpgsql;
CREATE TRIGGER ad_del AFTER DELETE ON ad FOR EACH ROW EXECUTE FUNCTION ad_del();


CREATE OR REPLACE FUNCTION vpn_upd() returns trigger as
$vpn_upd_trg$
BEGIN
    IF OLD.price!=NEW.price OR OLD.minFiat!=NEW.minFiat OR OLD.maxFiat!=NEW.maxFiat THEN
        PERFORM pg_notify('vpns_upd', row_to_json(NEW)::varchar);
    END IF;
    RETURN NULL;
END
$vpn_upd_trg$ LANGUAGE plpgsql;
CREATE TRIGGER vpn_upd AFTER UPDATE ON vpn FOR EACH ROW EXECUTE FUNCTION vpn_upd();

CREATE OR REPLACE FUNCTION vpn_new() returns trigger as
$vpn_new_trg$
BEGIN
    PERFORM pg_notify('vpns_new', row_to_json(NEW)::varchar);
    RETURN NULL;
END
$vpn_new_trg$ LANGUAGE plpgsql;
CREATE TRIGGER vpn_new AFTER INSERT ON vpn FOR EACH ROW EXECUTE FUNCTION vpn_new();

CREATE OR REPLACE FUNCTION vpn_del() returns trigger as
$vpn_del_trg$
BEGIN
    PERFORM pg_notify('vpns_del', OLD.id::varchar);
    RETURN NULL;
END
$vpn_del_trg$ LANGUAGE plpgsql;
CREATE TRIGGER vpn_del AFTER DELETE ON vpn FOR EACH ROW EXECUTE FUNCTION vpn_del();
    """)


if __name__ == "__main__":
    run(main())
