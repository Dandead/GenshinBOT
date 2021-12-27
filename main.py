from wishes import User
import asyncio
import telegram
import time
import aiofiles
from decorators import GLOBAL_LOOP

links = [
"https://webstatic-sea.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=13d0c223ab4131d488fae6508cd2c564c871b2&timestamp=1637711104&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A-3092.042724609375%2C%22y%22%3A252.1300048828125%2C%22z%22%3A-4426.61865234375%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5220062&plat_type=android&region=os_euro&authkey=SucW6ln%2FgKYnXC2jhnk7K9f%2BFycmx66pjLOHtuGi%2BGDP513zUy%2FzbNkvuV6CCOp%2FMup0k1J0l8%2FmK8FXy2bspZtSVE%2Bmuf%2Fgv5gUJJblyzy4Zzrn60Plm8sMS8B6%2BuAwrEP1Af6eagTiDQ%2B99ibRWttF4eieNQUKg03pXT3XxHmtTff%2F3isbDp32OmTgEIqrwNAX2h6K%2FWKxJHbH%2BLn4X%2FEh5oILykdJ%2Bw0TvlXq6e5KcjjkeXzUaoaw4zkV3Ip32TdMZSqvD6vslC4evmMK04OJfXTAyWNT%2BQhImrbtOohJHoXCP4WoNvvcazdKXyNnmQqhi%2F41JgDqHJ4B5e%2FHPe7EzHSnMk%2B1pfQIzzfQqp5PzEcZlDnXrYRpVh44EipOrA6Fu7G1yN01f4%2FyOk6zOi9tEzSTmJSU9ejG7aaf3JYZfX8UMnKYjmi%2Fb1%2FHXFVG%2BF3r7JYmwCWPQCKWbQtJdF5EVQSnX0AmUPf50ro9%2FMDeI537OTGDdSiIAUVDeJkrrytaBIlYNlqocgQ8wXghuKakrpMn1ouky%2F7Le1M7etkoPPBCRv0D5G8VJe3VHJ%2FFN0ErmSM%2BAfOp7ElpmPu3eXZg%2B9zvH%2FjG4pYEaw7kd5VkIGMW2OPnbvdRfinoJ5BenH1Bagi1ZTnNnCE5oGXE5OxqQgH7n2Ex%2BqAkiLIAe6EsvXMfziBIz13VpoiS6MJG%2BcA5cxLXlyhQ0%2FPEwuKmBYcNa5QPZPSK8pwCcs3trUhyNoLf56OIAvHqBH4KxFYTGN%2BAieskHTuhKPXYrV7Cx3DT5FbJYed821UesZNMsl5VxmL45dycT992XVz%2BR%2F0SLly6z12VhaJ0WNkBpTLIrx%2FRHyz3%2F%2F38thCMk%2B5mIiRC%2BmAD6OUBJCL98EuV2ViDNs2czJlD5s8xx93Sy5DOAmE0zuKL95CPzBA%2BhuShC5ErxCQ9hyuzv7jBPLcWuUN%2Fz6mLoLKrTRVj30J8eApFgw11EsXPBDSBUMiGRjDOUcVZcnLcGTyGdGwi669XdSzAkLo2D%2B8n01IpQGw%2F4QabVWb5uNx3LKIk8cyJAzAHdQ8eTPAFerWwNRSvbu8CXRjLqE4KH7S4Kehf%2Fxr8Apr6Ehuy5qehU4RZV2trIeS05Z7W5dXEn3c0jgA%2F7p63ETKiUg%2FMsCZhfLHsyFuu16BB%2B2hHxG3x1m2Diu%2BV1RTHJ1ePP0N3qz6m6ZJzQH2Wvf2boZiYIoJeTRVjnmpnsR9olw%2BmfjFq5SO12hg1Q8Cljg0RhOVf0ww1JwjY%2Bj4yZCSbb0JL1So2cbY9aDx%2F3rtYZtKk6uh5TqvC%2B%2BTxJxObX16YZ8p7A465gDNJUG%2BPEkVX%2FMI9j%2BNGHOODmXChsI5vgQ%3D%3D&game_biz=hk4e_global#/log",
"https://webstatic-sea.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=13d0c223ab4131d488fae6508cd2c564c871b2&timestamp=1637711104&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A-3092.042724609375%2C%22y%22%3A252.1300048828125%2C%22z%22%3A-4426.61865234375%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5220062&plat_type=android&region=os_euro&authkey=SucW6ln%2FgKYnXC2jhnk7K9f%2BFycmx66pjLOHtuGi%2BGDP513zUy%2FzbNkvuV6CCOp%2FMup0k1J0l8%2FmK8FXy2bspZtSVE%2Bmuf%2Fgv5gUJJblyzy4Zzrn60Plm8sMS8B6%2BuAwrEP1Af6eagTiDQ%2B99ibRWttF4eieNQUKg03pXT3XxHmtTff%2F3isbDp32OmTgEIqrwNAX2h6K%2FWKxJHbH%2BLn4X%2FEh5oILykdJ%2Bw0TvlXq6e5KcjjkeXzUaoaw4zkV3Ip32TdMZSqvD6vslC4evmMK04OJfXTAyWNT%2BQhImrbtOohJHoXCP4WoNvvcazdKXyNnmQqhi%2F41JgDqHJ4B5e%2FHPe7EzHSnMk%2B1pfQIzzfQqp5PzEcZlDnXrYRpVh44EipOrA6Fu7G1yN01f4%2FyOk6zOi9tEzSTmJSU9ejG7aaf3JYZfX8UMnKYjmi%2Fb1%2FHXFVG%2BF3r7JYmwCWPQCKWbQtJdF5EVQSnX0AmUPf50ro9%2FMDeI537OTGDdSiIAUVDeJkrrytaBIlYNlqocgQ8wXghuKakrpMn1ouky%2F7Le1M7etkoPPBCRv0D5G8VJe3VHJ%2FFN0ErmSM%2BAfOp7ElpmPu3eXZg%2B9zvH%2FjG4pYEaw7kd5VkIGMW2OPnbvdRfinoJ5BenH1Bagi1ZTnNnCE5oGXE5OxqQgH7n2Ex%2BqAkiLIAe6EsvXMfziBIz13VpoiS6MJG%2BcA5cxLXlyhQ0%2FPEwuKmBYcNa5QPZPSK8pwCcs3trUhyNoLf56OIAvHqBH4KxFYTGN%2BAieskHTuhKPXYrV7Cx3DT5FbJYed821UesZNMsl5VxmL45dycT992XVz%2BR%2F0SLly6z12VhaJ0WNkBpTLIrx%2FRHyz3%2F%2F38thCMk%2B5mIiRC%2BmAD6OUBJCL98EuV2ViDNs2czJlD5s8xx93Sy5DOAmE0zuKL95CPzBA%2BhuShC5ErxCQ9hyuzv7jBPLcWuUN%2Fz6mLoLKrTRVj30J8eApFgw11EsXPBDSBUMiGRjDOUcVZcnLcGTyGdGwi669XdSzAkLo2D%2B8n01IpQGw%2F4QabVWb5uNx3LKIk8cyJAzAHdQ8eTPAFerWwNRSvbu8CXRjLqE4KH7S4Kehf%2Fxr8Apr6Ehuy5qehU4RZV2trIeS05Z7W5dXEn3c0jgA%2F7p63ETKiUg%2FMsCZhfLHsyFuu16BB%2B2hHxG3x1m2Diu%2BV1RTHJ1ePP0N3qz6m6ZJzQH2Wvf2boZiYIoJeTRVjnmpnsR9olw%2BmfjFq5SO12hg1Q8Cljg0RhOVf0ww1JwjY%2Bj4yZCSbb0JL1So2cbY9aDx%2F3rtYZtKk6uh5TqvC%2B%2BTxJxObX16YZ8p7A465gDNJUG%2BPEkVX%2FMI9j%2BNGHOODmXChsI5vgQ%3D%3D&game_biz=hk4e_global#/log",
"egsghtjnftjj",
"https://webstatic-sea.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=13d0c223ab4131d488fae6508cd2c564c871b2&timestamp=1637711104&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A-3089.126708984375%2C%22y%22%3A252.15164184570313%2C%22z%22%3A-4425.0830078125%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5220062&plat_type=android&region=os_euro&authkey=xf2lRTcwB3bgaB%2FpsF27R0YceGj1aNOjpNWLCi3e0iDx1CIB9hSKAL5SxWmuUGCTOKHN%2BclA6tay5IDdrK9poXYDq1diZiPcjkJuYh%2B9uy0iMzsU3nSJGVJbwCsRwOOISMsTgGSNgnDYwsICEGtCPQdM%2Bom84dn9t1LYabucRsjP81vO0uU74ndpnSCQA1Twf1qgGJrpF%2FwzCF9FIl3dOeVqxxKSw3o48cE%2FqJ5E%2BXqOuXLoEPZrtFlFksvruvUCTwHC3vZvc%2FCe%2FSPR4bICmia0dEpT3XIASXKP7m%2FXsovPXqYfZ13oYYXUL1J27vxe78KFx42uvfZrUpc5Xwo8E%2B7EzHSnMk%2B1pfQIzzfQqp5PzEcZlDnXrYRpVh44EipOrA6Fu7G1yN01f4%2FyOk6zOi9tEzSTmJSU9ejG7aaf3JYZfX8UMnKYjmi%2Fb1%2FHXFVG%2BF3r7JYmwCWPQCKWbQtJdF5EVQSnX0AmUPf50ro9%2FMDeI537OTGDdSiIAUVDeJkrrytaBIlYNlqocgQ8wXghuKakrpMn1ouky%2F7Le1M7etkoPPBCRv0D5G8VJe3VHJ%2FFN0ErmSM%2BAfOp7ElpmPu3eXZg%2B9zvH%2FjG4pYEaw7kd5VkIGMW2OPnbvdRfinoJ5BenH1Bagi1ZTnNnCE5oGXE5OxqQgH7n2Ex%2BqAkiLIAe6EgGmBKo3iLuBO%2B28YTBE7XoJYtlT%2FJv9Tn8L4yzhSFgg%2Bz2X%2F2JGn7J6J7vvzDmNz3LTMbsxgkYPcHlgBJRnXDujVmDoC37EztXt1H%2FavQRctJEuSXCJhEpQvwb32oMt44wgAirqngnjdSoFlfm%2F5vt6AL7RfzPxA5QfWoE3TULqM0khj5ebgnyrS8KaPYOb%2BcE6A%2F%2BfdgQVnfQcs6ec7q2AtRo%2BfmxEaftfwUGUpXnmoMnq6e3nVwB0MYJm6ZM45Cuq0v%2BITiYs00BBYbMfWdrsMNQoxIu2MLXzNrAmbEuyv1m1M6Qw7i81Y%2FCnumFjE06uP4W4HGoA%2FPoJ36sEFrYKgHXWp2hs8sSS0jzRjsxAaXz3bN0UHcM3s%2BASGwi0A8E%2BbyTxguWGSdOFokdBcU%2B8QHPZu%2BY%2BlsgjANOASZ7qBdkGg8cv7MY9iKh3ILsK1NvNs7jHDgYlNfkDWu7BcpZDx6Lge0%2FfV%2Fzw6Lyvu7A%2F5HyS8sfxFS3l9lorvnJEkbFA8zwR%2FuvlB4P2xcdo%2Bjl%2FVlbo9TKRdOiDOKzkDMM37foNrZr7XlKMeNT6jSAPuRlgTVVp2EiWCfQN43fBTxeVzS5Mk8ZkEi49Et1P1kWo8HBo0JnDeVHY0zloRNShhapClCKA%2BAAkU381a922MVGqUrxiscylPzOrVO4aUsYQ%3D%3D&game_biz=hk4e_global#/log",
"https://webstatic-sea.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=13d0c223ab4131d488fae6508cd2c564c871b2&timestamp=1637711104&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A1039.0103759765625%2C%22y%22%3A450.198486328125%2C%22z%22%3A-823.1796264648438%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5146901&plat_type=android&region=os_euro&authkey=xf2lRTcwB3bgaB%2FpsF27R0YceGj1aNOjpNWLCi3e0iDx1CIB9hSKAL5SxWmuUGCTOKHN%2BclA6tay5IDdrK9poXYDq1diZiPcjkJuYh%2B9uy0iMzsU3nSJGVJbwCsRwOOISMsTgGSNgnDYwsICEGtCPQdM%2Bom84dn9t1LYabucRsjP81vO0uU74ndpnSCQA1Twf1qgGJrpF%2FwzCF9FIl3dOeVqxxKSw3o48cE%2FqJ5E%2BXqOuXLoEPZrtFlFksvruvUCTwHC3vZvc%2FCe%2FSPR4bICmia0dEpT3XIASXKP7m%2FXsovPXqYfZ13oYYXUL1J27vxe78KFx42uvfZrUpc5Xwo8E%2B7EzHSnMk%2B1pfQIzzfQqp5PzEcZlDnXrYRpVh44EipOrA6Fu7G1yN01f4%2FyOk6zOi9tEzSTmJSU9ejG7aaf3JYZfX8UMnKYjmi%2Fb1%2FHXFVG%2BF3r7JYmwCWPQCKWbQtJdF5EVQSnX0AmUPf50ro9%2FMDeI537OTGDdSiIAUVDeJkrrytaBIlYNlqocgQ8wXghuKakrpMn1ouky%2F7Le1M7etkoPPBCRv0D5G8VJe3VHJ%2FFN0ErmSM%2BAfOp7ElpmPu3eXZg%2B9zvH%2FjG4pYEaw7kd5VkIGMW2OPnbvdRfinoJ5BenH1Bagi1ZTnNnCE5oGXE5OxqQgH7n2Ex%2BqAkiLIAe6EgGmBKo3iLuBO%2B28YTBE7XoJYtlT%2FJv9Tn8L4yzhSFgg%2Bz2X%2F2JGn7J6J7vvzDmNz3LTMbsxgkYPcHlgBJRnXDujVmDoC37EztXt1H%2FavQRctJEuSXCJhEpQvwb32oMt44wgAirqngnjdSoFlfm%2F5vt6AL7RfzPxA5QfWoE3TULqM0khj5ebgnyrS8KaPYOb%2BcE6A%2F%2BfdgQVnfQcs6ec7q2AtRo%2BfmxEaftfwUGUpXnmoMnq6e3nVwB0MYJm6ZM45Cuq0v%2BITiYs00BBYbMfWdrsMNQoxIu2MLXzNrAmbEuyv1m1M6Qw7i81Y%2FCnumFjE06uP4W4HGoA%2FPoJ36sEFru6Zwz03bFhdM8qF3oa7aop95hwbiqJ5HkfsZ0qJDudkkWgfQACqdTMw0j%2FgqPO24SpU85VKZ25eokiIeKuRR4vyxhNf76jS%2BNrJJvwqKegNCyt5cWCoB91yLADBW5hQKXKUZzLT6oNNsO8esz3wEpMQAb4ex32fu0chFv2Og2VJDTcgHcrILusOydLf%2Bxf1MsxnyJpas8VKIR2P0OenQ1Zr4TYlEU0T3%2ByEEDFGVT4yqedVcG7hM7zuu1r%2Bos0bwL%2FWeky4zHunTlCCG%2BuxHxGSrgyneOG021NFg1H0wOAdV9ZZijpOBLM3Wa8%2B%2FBAV5kMx%2BetD2D7%2FX9DfbUntMEw%3D%3D&game_biz=hk4e_global#/log",
"https://webstatic-sea.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=13d0c223ab4131d488fae6508cd2c564c871b2&timestamp=1637711104&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A1462.414306640625%2C%22y%22%3A267.7742614746094%2C%22z%22%3A-632.916748046875%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5146901&plat_type=android&region=os_euro&authkey=KisonuvOjkxaMFtjDxZKqHIZEyM1OgDTCYsYRTFJUb5AFIr3ZMI9Z8NJprOqKf1%2BaRtFlMkt%2FcVSzDMwg7TTt1SbDeILIggpy9vkCeehMyvjZk2TMgSHR7N9cbYiVAhSQKadOxWcrSSCIy5OMhVM%2Bqvc3SqyYh5a5tVv6M9xRzRYo1TWibkGUGu8ob2%2BqUYg%2B41AnDSw6Mj4EJ%2FvDY7N3M5V1m63HmH1yOMRrR1%2BVg9lOYKcehFoFUPu2PEJ8uTaQniG3lzJkVzGp0nzYAYMAMXbkdNXiBi6VUMP5LrRfFi5lVsEefkk7b6f2lQMIjdGlvQuwuvX04gBqxS5%2FAc5ZwB4scXxe%2BL7pvUvE534woBOoytyuzoZbHAsNanHKSwOZ9D7GpUsbSYlz8I74vG%2Fo3uUG8F7t8HgzBuXLo3DxuaejWhEQuvgZ1RlrgPjQ0zpnyAS62ABY3QZJUZmN5kThi6CwGimq6AjPavibVrV1FWm7pGZq8vlMNiKmT98RvemiFZDfjQDEVPQHeEok8a%2BoM2emZX25hUbPDfZBDf8HVeQmL%2FQ39DwXdKDrqPbdo99KuDsC%2B6yY88fU9rwBmS6B51YxboymvTJ5tgbMNZ5DViChK57VOntqR3NnMoqCKKqnfVmMsX1NZFOEkJaf0eGenw5cFA6hLYpTiFjXIOkjhdIPOjS4PyZQkrlwocx4THiIhs6bkIwjE4AiimVEGC0Sn6SKuYTxHncMBJiNhGsM6PrZB5l6iHGMXAeOb7AWkqvk80fM%2BbVTunufKYc3rHMgHYTR%2F6l6HBMEvDMzxWHPOcSXpbm6rQxRAjtFDBTDLjXEkOhOl%2FxoGqIfhq3xqm1Cfks9mnqJq92AAOigsPvVpMXwviWzmcsxRNpMz%2FT60cfrf%2Fw9bq2hCCNBycLC7v8m4L9OhmyhZQ3N5ApmxPmhNBUzzmgNFUpf4IRGO%2Fi%2BxfxMSourAjv8j14vhBNlpC5hHcJs49q%2Bc9J9yP0PfGkQoEnqT6ogyXJmNwQK5ze1x3rtBsfeC1wJQN4GIBOugbogGU07Q3pJoIrLfbuR%2BdFObLBbYS%2FSa1PuwDSirUV%2B8Y3K1Fx25WZcP0SGVhSyqu1IexvmF40mTJo6X35rY4lEKSmFHY4PfPFHtxPmi32NcUYdj5TP3qrA%2BFBl1i2jwzfENyfvaaea3UM2JiN%2FibNCiz%2BmOvKCkusXrSEfq%2BP%2FdJw7CzSGs%2FotL0rnp1HB7IyHpkc2NEH46wVdRjeFWlE1ZlPzUuI9HMpL4Xl0sBZ%2FcTvpBhGRX2qyaToHTZ7%2Bpzs0k7LAGYf%2BvQymRPhdAbyGQKuHilDRdUTB9H09rGsrviuS6J6wnwcRk9ZmRegqtQW2Q%3D%3D&game_biz=hk4e_global#/log",
"https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?im_out=false&sign_type=2&auth_appid=im_ccs&authkey_ver=1&win_direction=portrait&lang=ru&device_type=mobile&ext=%7B%22loc%22%3A%7B%22x%22%3A2257.82080078125%2C%22y%22%3A272.1188659667969%2C%22z%22%3A-246.96726989746095%7D%2C%22platform%22%3A%22Android%22%7D&game_version=OSRELAndroid2.3.0_R5134813_S5082883_D5146901&plat_type=android&authkey=KMfIBUAQNgBzs6aAnZ7AfAtTNaM%2FukwH9f9fKpivl%2Bs9CuVR8CQ96DCUQ9CkbvfvY4AlkhUfLd6U3tqt%2BOiaZYDiUhH0DWlyQQIkAYrEI0%2BamQvliiR9HFbtgVR26INzW%2FhbIH8pZsfv1tolAYR7popKvVdLxARCL3SKpasvdTatZdWHMuZ9EDs4zjON2wQ%2Fcfhz0NTBPJoYrr6hitu%2FHH%2BhlJODUfo%2FiNyweiBK%2Bai7gXvMl1TQ%2BdnJZzgisobnFpO4sSCUXkc0bPW5ln8c8EhIxdmpuZ%2FqsNb865nsiWWD06WcTNc9E0US5njhTyViQ6mGXDvA6fqF10W%2FgAvM72jeS1oWe8nAkPCIW4AE6mXE5RkESwQxm2k5eingl3Lgfm%2B018S4y9OJlpXNsDVno8bgATCiIfW4G%2Bw000qC4tFCNE3%2BT9Vma1uXUE4gd0c2SMRI3TlBvr9WNCwzLkxChKAoOWLEw77W8mB%2BlQJVZhzPT0tt4AAe5toNdm5Le9LR3Xw8ec9V8nz0impveQhQMYArkH0YIi7fEReUNpPQda1I1Y%2B9mzglYe60741DNQucjjxxVy4pXCOvc86neWcJCIwT6Si958CKXVe%2BnYObMz%2BaVIIhqEUtqZLCQmvtsxAd8IDBiGKshbhKD9SQcreEqtYNk2DUHtlGqO0HVjOzLSvOENUivCLiRG6a5HHzMp3Y2ADUS6sF459Wa1QGA7%2BdnwoF0zAZLxwinvhX1CdCSK5yMwfnjEllBG6FdoL9MZfwUZTIPg7sSTBK%2FM%2Bg64b59Uhphn7%2BtdiVFoKLpGkRU5oXSIKDevjucpjYOmfdqmqzFtQqD89RjO9Y4l62JXbGE%2FwUpjbP2oTlReu1NYyj%2B9Ig2dPxQ4hbvACFcV73wq26gj2Kyih7A4obJZwsQzavEKSqoJcxW%2FGXFKIxB4l1IxfRTJMAcP4trJ0Qjz20ibAZY7y2jlIRn%2B2j4guX%2FDQN%2FNbH%2FfwpK%2BvCwUdOScYdsKFfLeBMU2fBByNU2V316DBbqGs6WxP4VduO2w%2BBDOycz0xD19pCPte6IL961CVAyLEKTIXoS%2FicPqbQuuwWGHsZqhn4hMNONeJulcUSrcODcw0nxxppF2%2F3I8Fh%2FErBTFLbmFlKVkbD0Z4ojAxv0a4eFFwLeLBqaSz8gxM4WMoc%2BDC%2BfSucB9CArdE1e6bD3c%2Bcr0ZdyNdphjyQ9ZnZzkesDuhfx1UmxPplvkXKQdEWYgwmvR4t7INOmylntaHfbA0pEWvKmRPL2QkNsQiFItU%2FddUcZEoOSYo83t0JJXw%2BCBvm7DRJamG0EtBRiEjXRdR7fugPZgODaNph1fkcD8OwXlwemVUrM6lX47dno0xARQ%3D%3D&game_biz=hk4e_global#/"

]


async def main():
	while True:
		# async with aiofiles.open("./config/curent_link.txt", "r") as e:
		# 	lines = await e.readlines()
		# with open("./config/curent_link.txt", "w"):
		# 	pass
		# if lines:
			for line in links:
				new = User(line)
				if new:
					asyncio.ensure_future(new.start_update_db())
					# await new.start_update_db()
				# print(GLOBAL_LOOP)
				await asyncio.sleep(2)
		# await asyncio.sleep(15)
		# print(time.asctime()+" New iteration")

asyncio.run(main())
