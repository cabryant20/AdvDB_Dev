<p>Update Task</p>
<form action="/update_item/{{row[0]}}" method="POST">
    <input type="text" size="100" maxlength="100" name="update_item" value="{{row[1]}}">
    <input type="submit" name="save" value="Update">
</form>