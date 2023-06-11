import datetime
dt = '21/03/2012'
day, month, year = (int(x) for x in dt.split('/'))    
ans = datetime.date(year, month, day)
print (ans.strftime("%A"))
print(f'<p id="gender"><img src="{{{{ url_for("static", filename = "img/gender-fluid.png")}}}}" alt="Sport Icon">Gender</p>')