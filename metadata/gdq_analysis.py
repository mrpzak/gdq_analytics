import gdq_functions as func
import matplotlib.pyplot as plt

repo_path=r"C:\repos\gdq\agdq2020\reports"
filename="GDQ_Schedule"

# Check if file exists; if so, delete and create a
# blank version with just column names.

func.check_file(repo_path,filename)

# Loops through the GDQ website, using the index 
# as part of the website address, and pull the 
# schedule in, and append to df and csv.
# URL structure is gamesdonequick/schedule/<index>

i=17
while i<=28:
    try:
        if i==17:
            game_list=func.get_schedule(repo_path,filename,i)
        else:
            game_list=game_list.append(func.get_schedule(repo_path,filename,i))
    except:
        print("Page not found")
    i+=1

# Standardizes the names for consoles, i.e.
# "Nintendo DS" renamed as "NDS"

game_list=func.platform_cleanup(game_list)

# Summarize list of games by platform, and sort
# descending, getting the top 10, and then graphing.

platform_list=game_list.groupby('Platform')['Game'].count()
platform_list=platform_list.to_frame()
plat_sort=platform_list.sort_values(by='Game',ascending=False).head(10)

# Summarize number of games run in each event and graphing.

event_list=game_list.groupby('Event')['Game'].count()
event_list=event_list.to_frame()

plat_sort.plot(kind="bar")

plt.title("Top 10 Consoles from GDQ Runs")
plt.legend().remove()
plt.savefig(repo_path+"\\top_gdq_consoles.png")

event_list.plot(kind="bar")
plt.title("Number of Games by Event")
plt.legend().remove()
plt.savefig(repo_path+"\\game_by_event.png")
