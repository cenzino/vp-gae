"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""


from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

from models import ExampleModel, Post, Category
from decorators import login_required, admin_required
from forms import ExampleForm, PostForm, PostForm2
from flaskext import wtf


def home():
    return redirect(url_for('list_posts'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

def list_posts():
    posts = Post.all()
    return render_template('list_posts.html', posts=posts)

def new_post():
    #form = PostForm()
    form = PostForm2()
    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            category = form.category.data,
            tags = Post.convert_string_tags(form.tags.data),
        )        
        try:
            post.put()
            flash(u'Example %s successfully saved.' % post.id, 'success')
            return redirect(url_for('list_posts'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_posts'))
    return render_template('new_post.html', form=form)

def edit_post(post_id):
    post = Post.get_by_id(post_id)
    form = PostForm2(obj=post)
    
    if form.validate_on_submit():
        form.tags.data = Post.convert_string_tags(form.tags.data)
        form.populate_obj(post)
        try:
            post.put()
            flash(u'Example %s successfully saved.' % post.id, 'success')
            return redirect(url_for('list_posts'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_posts'))
    return render_template('edit_post.html', form=form, post_id=post_id)

def save_post():
    pass

@login_required
def delete_post(post_id):
    """Delete an post object"""
    post = Post.get_by_id(post_id)
    try:
        post.delete()
        flash(u'Example %s successfully deleted.' % post_id, 'success')
        return redirect(url_for('list_posts'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_posts'))

@login_required
def list_examples():
    """List all examples"""
    examples = ExampleModel.all()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name = form.example_name.data,
            example_description = form.example_description.data,
            added_by = users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key().id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)
    try:
        example.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
        return redirect(url_for('list_examples'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_examples'))


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''