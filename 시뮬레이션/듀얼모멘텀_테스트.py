import Analyzer
import dualmomentum


# = Analyzer.MarketDB()
momentum = dualmomentum.DualMomentum()
x = momentum.get_rltv_momentum("2022-04-05","2022-07-05",5)
y = momentum.get_abs_momentum(x,"2022-07-05","2022-10-05")
print(y)
