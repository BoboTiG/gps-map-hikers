<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <title>Trek | Photo</title>
    <link href="favicon.png" rel="icon" type="image/x-icon">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <link rel="stylesheet" href="assets/css/app.css" />
</head>

<body>
<form action="picture/upload" method="post" enctype="multipart/form-data">
  <label for="trace">Trace</label>
  <select name="trace">
    %for trace in reversed(traces):
    %if trace["pic"]:
    <option value="{{ trace["ts"] }}">✧ {{ trace["date"] }}</option>
    %else:
    <option value="{{ trace["ts"] }}">{{ trace["date"] }} </option>
    %end
    %end
  </select> 
  <br>
  <label for="picture">Photo</label>
  <input type="file" name="picture" />
  <br>
  <br>
  <button type="submit">Envoyer</button>
  <p>✧ Une photo est déjà assignée à la trace et sera écrasée.</p>
</form>

</body>

</html>
