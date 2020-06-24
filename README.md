# Visualize reveal.js tracking data

This python flask (web-)application is made to visualize anonymized reveal.js tracking data in a dashboard.
The data is being tracked by the [reveal.js tracking plugin](https://github.com/pantajosef/reveal.js-tracking)
and anonymized by the [anonymizeReveal.js application](https://github.com/jquku/anonymizeReveal.js) using the ARX data anonymization tool.

#### Prerequisites (installation via pip is recommended)
- python flask
- requests

#### Changes in reveal.js tracking plugin

The data for the dashboard is being stored in a postgreSQL database.
An interface is being used to receive the data by a route. In order to make it 
work the following route needs to be added in the app.rb file in the [reveal.js tracking plugin](https://github.com/pantajosef/reveal.js-tracking).

```
#ADDED: new route that returns a json object with data for every tracked session
get '/all' do 
  students = Student.all()
  tracked_sessions = TrackedSession.all()

  tracking_json =  tracked_sessions.order(created_at: :desc).all
  tracking_json.to_json
end 
```

#### Still missing
- filtering of modules and lectures in a database
- video data
- audio data

Important: Since no strategy concerning the frequency of data anonymization has been chosen, this application still uses the datasets
who are not k-anonymized yet. In order to only select the anonymized database table as a data basis, only the additional reveal.js tracking plugin
route needs to be adjusted accordingly.
