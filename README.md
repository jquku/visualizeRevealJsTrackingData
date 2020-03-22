# AnonymizeEducationalData

This (web-)application is made to anonymize education data from a reaveal.js 
presentation. 

#### Changes in reveal.js tracking plugin

in app.rb added new route

```
#ADDED: new route that returns a json object with data for every tracked session
get '/all' do 
  students = Student.all()
  tracked_sessions = TrackedSession.all()

  tracking_json =  tracked_sessions.order(created_at: :desc).all
  tracking_json.to_json
end 
```