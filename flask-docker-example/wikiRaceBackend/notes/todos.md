# Project TODOs

The Project will be a Flask Backend connected to the React Frontend using CORS. To do this, the backend must be rewritten in Flask.

- Flask Backend:
  - Set up Endpoints
  - Create Templates to serve to the frontend

## Notes

- Top-level `__init__.py` file in the `/app` directory is used to instantiate the app, and any configs needed are pulled from the config.py file.

- Routes and Endpoints are defined in the `/routes` directory, with `page_routes.py` containing each of the pages that the user could visit

- Dynamic Routes can be set like this:

```python
# Dynamic route for tag
@bp.route('/posts/<tag>')
def post_by_tag(tag):
    # Here you could fetch the actual post(s) based on the tag
    # For demonstration purposes, just passing the tag to the template
    return render_template('post.html', tag=tag)
```
