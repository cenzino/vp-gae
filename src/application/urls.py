"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

# Say hello
app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)

# Examples list page
app.add_url_rule('/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# Contrived admin-only view example
app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# Delete an example (post method only)
app.add_url_rule('/examples/delete/<int:example_id>', view_func=views.delete_example, methods=['POST'])


# Posts list page
app.add_url_rule('/posts', 'list_posts', view_func=views.list_posts, methods=['GET', 'POST'])
# Posts list page
app.add_url_rule('/posts/new', 'new_post', view_func=views.new_post, methods=['GET', 'POST'])
app.add_url_rule('/posts/edit/<int:post_id>', view_func=views.edit_post, methods=['POST'])
app.add_url_rule('/posts/delete/<int:post_id>', view_func=views.delete_post, methods=['GET','POST'])

app.add_url_rule('/editor/', 'editor', defaults={'post_id': None}, view_func=views.editor, methods=['GET','POST'])
app.add_url_rule('/editor/<int:post_id>', view_func=views.editor, methods=['GET', 'POST'])

app.add_url_rule('/categories', 'list_categories', view_func=views.list_categories, methods=['GET', 'POST'])
app.add_url_rule('/categories/new', 'new_category', view_func=views.new_category, methods=['GET', 'POST'])
app.add_url_rule('/categories/delete/<string:category_name>', view_func=views.delete_category, methods=['POST'])
app.add_url_rule('/categories/edit/<string:category_name>', view_func=views.edit_category, methods=['POST'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

