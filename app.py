"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

#with app.app_context():
#        db.drop_all()
#        db.create_all()

@app.route('/')
def home():
    with app.app_context():
        return redirect('/users')
    
@app.route('/users')
def users_page():
    with app.app_context():
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_page(user_id):
    with app.app_context():
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter(Post.user_id == user_id)
        return render_template('user.html', user=user, posts=posts)
    
@app.route('/users/new')
def create_user_page():
    return render_template('create-user.html')

@app.route('/users/new', methods=['POST'])
def update_new_user():
    with app.app_context():
        #creates new User instance
        new_user = User(first_name=request.form.get('first_name'),
                         last_name=request.form.get('last_name'), 
                         image_url=request.form['image_url'] or None)
        #adds new user to db and comits it
        db.session.add(new_user)
        db.session.commit()
        #redirects to users page
        return redirect('/users')
    
@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    with app.app_context():
        user = User.query.get_or_404(user_id)
        return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        # Update user with form data
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url', 'default-profile.jpg')
        # Commit the changes
        db.session.commit()
        # Redirect to the user page
        return redirect(f'/users/{user_id}')
    
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    
@app.route('/users/<int:user_id>/posts/new')
def show_form(user_id):
    """Show form to add a post for that user."""
    with app.app_context():
        #gets user
        user = User.query.get_or_404(user_id)
        #gets all tags
        tags = Tag.query.all()
        return render_template('add-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    with app.app_context():
        #creates new post and adds it
        
        new_post = Post(title=request.form.get('title'),
                        content=request.form.get('content'),
                        user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        #ADDS POST TAGS
        #gets tags list
        tags=request.form.getlist('tags')
        for tag in tags:
            new_post_tag = PostTag(post_id=new_post.id,
                               tag_id=int(tag))
            db.session.add(new_post_tag)
        db.session.commit()
        return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    with app.app_context():
        post = Post.query.get(post_id)
        tags = post.tags
        return render_template('show-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    with app.app_context():
        post = Post.query.get(post_id)
        all_tags = Tag.query.all()
        post_tags = post.tags
        return render_template('edit-post.html', post=post, all_tags=all_tags, post_tags=post_tags)
    
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    with app.app_context():
        #updates title and content
        post = Post.query.get(post_id)
        post.title = request.form.get('title')
        post.content = request.form.get('content')

        #gets new tags list
        tags=request.form.getlist('tags')
        #deletes all current tags and adds new ones
        PostTag.query.filter_by(post_id=1).delete()
        db.session.commit()
        for tag in tags:
            new_post_tag = PostTag(post_id=post_id,
                               tag_id=int(tag))
            db.session.add(new_post_tag)

        db.session.commit()
        return redirect(f'/posts/{post_id}')
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def show_tags():
    """Lists all tags, with links to the tag detail page."""
    with app.app_context():
        tags = Tag.query.all()
        return render_template('show-tags.html', tags=tags)

@app.route('/tags/new')
def show_tag_form():
    """Shows a form to add a new tag."""
    return render_template('tag-form.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
    """Shows a form to add a new tag."""
    with app.app_context():
        #creates new Tag instance
        new_tag = Tag(name=request.form.get('tag_name'))
        #adds new user to db and comits it
        db.session.add(new_tag)
        db.session.commit()
        #redirects to users page
        return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_page(tag_id):
    """ Show detail about a tag. Have links to edit form and to delete."""
    with app.app_context():
        tag = Tag.query.get_or_404(tag_id)
        posts = tag.posts
        return render_template('tag-info.html', tag=tag, posts=posts)
    
@app.route('/tags/<int:tag_id>/edit')
def show_edit_form(tag_id):
    """Show edit form for a tag."""
    with app.app_context():
        tag = Tag.query.get_or_404(tag_id)
        return render_template('edit-tag.html', tag=tag)
    
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_form(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""
    with app.app_context():
        tag = Tag.query.get_or_404(tag_id)
        # Update tag with form data
        tag.name = request.form.get('tag_name')
        # Commit the changes
        db.session.commit()
        # Redirect to the user page
        return redirect(f'/tags/{tag_id}')
    
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    with app.app_context():
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect('/tags')
