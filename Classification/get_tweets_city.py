import twint

c = twint.Config()

key_dict=['covid','corona','quarantine','lockdown','social-distanc']
city_dict=["19.071217, 72.929863,23km","28.620521, 77.222534,10km","12.962140, 77.584252,27km","26.881156, 75.802712,16km","23.029942, 72.581648,13km"]
for x in city_dict:
	for y in key_dict:
		c.Search = y
		c.Geo = x
		c.Limit = 800
		c.Store_csv = True
		c.Hide_output = True
		c.Output = "tweets_raw.csv"
		twint.run.Search(c)
