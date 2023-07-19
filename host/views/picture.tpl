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
<form action="picture/upload", method="post" enctype="multipart/form-data">
  <label for="trace">Choisir une trace</label>
  <input list="traces" name="trace" autocomplete="off">
  <datalist id="traces">
    %for trace in reversed(traces):
    <option value="{{ trace["ts"] }}">{{ trace["date"] }}</option>
    %end
  </datalist> 
  <br>
  <br>
  <label for="picture">Choisir une photo</label>
  <input type="file" name="picture">
  <br>
  <br>
  <button type="submit">Envoyer</button>
</form>
</body>

</html>
