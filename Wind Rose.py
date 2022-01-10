from Load_Data import winds_df
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from windrose import WindroseAxes

wd = winds_df['WD_avg']
ws = winds_df['WS_avg']
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
ax.set_xticklabels (['E', 'NE', 'N', 'NW',  'W', 'SW', 'S', 'SE'], fontsize=14)
plt.title('Wind Direction and Speed (m/s)', fontsize=24)
plt.show()