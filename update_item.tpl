<p>Update Task</p>
<form action="/update_item" method="POST">
    <input type="text" size="100" maxlength="100" name="update_item" value="{{row[1]}}">
    <input type="hidden" size="100" name="id" value="{{row[0]}}">
    <input type="submit" name="save" value="Update">
</form>