import twint
import datetime

current_date = datetime.datetime(2020,3,20)
current_end_date = current_date + datetime.timedelta(days=1)
end_date = datetime.datetime(2020,4,10)
key_dict=['covid','corona','quarantine','lockdown','nike','adidas']
city_dict=["19.071217, 72.929863,23km","28.620521, 77.222534,10km","12.962140, 77.584252,27km","26.881156, 75.802712,16km","23.029942, 72.581648,13km"]
while (current_date != end_date):
	for x in key_dict:
		for y in city_dict:
			c = twint.Config()
			c.Search = x
			c.Geo = y
			c.Limit = 40
			c.Store_csv = True
			c.Output = 'tweets_raw.csv'
			c.Hide_output = True
			c.Since = current_date.strftime("%Y-%m-%d")
			c.Until = current_end_date.strftime("%Y-%m-%d")
			c.Filter_retweets = True
			twint.run.Search(c)
	print(current_date)
	current_date = current_end_date
	current_end_date += datetime.timedelta(days=1)
print(current_date != end_date)

