from unittest import TestCase
from app import app
from models import User, Post, db

app.config['SQLALCHEMY_DATABSE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

class RouteTests(TestCase):

    def setUp(self):
        """Does before each"""
        with app.app_context():
            self.client = app.test_client()
            app.config['TESTING'] = True

    def test_users_page(self):
        """Make sure users page HTML is displayed"""
        with self.client:
            res = self.client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)
            self.assertIn('<button class="green">Add User</button>', html)

    def test_home_redirect(self):
        """Makes sure home page redirects to users page"""
        with self.client:
            res = self.client.get('/')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/users')

    def test_home_redirect_followed(self):
        """Makes sure redirect to users page's html is displayed"""
        with self.client:
            res = self.client.get('/', follow_redirects = True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)
            self.assertIn('<button class="green">Add User</button>', html)


class UsersModelTests(TestCase):

    def setUp(self):
        """Cleans up exisintg users and adds new user"""
        with app.app_context():
            self.client = app.test_client()
            app.config['TESTING'] = True
    
            User.query.delete()
            db.session.commit()

            user1 = User(first_name = "Joe", last_name = "Jonas")
            db.session.add(user1)
            db.session.commit()
            self.user1_id = user1.id

    def tearDown(self):
        """Cleans up any failing transactions"""
        with app.app_context():
            db.session.rollback()

    def test_show_user1_on_users_page(self):
        """Makes sure user is added to users page"""
        with self.client:
            res = self.client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)
            self.assertIn('Joe Jonas', html)

    def test_show_user1_page(self):
        """Make sure user1 page is accessible"""
        with self.client:
            res = self.client.get(f'/users/{self.user1_id}')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Joe Jonas</h1>', html)
            self.assertIn('<button class="green">Add Post</button></a>', html)


    def test_show_edit_user_page(self):
        with self.client:
            res = self.client.get(f'/users/{self.user1_id}/edit')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="user-name">Joe Jonas</h1>', html)
            self.assertIn('<label>First Name:<input type="text" id="first_name" name="first_name" required value="Joe"></label>', html)

        

class PostsModelTests(TestCase):

    def setUp(self):
        """Cleans up exisitng posts"""
        with app.app_context():
            self.client = app.test_client()
            app.config['TESTING'] = True

            Post.query.delete()
            db.session.commit()
            
            User.query.delete()
            db.session.commit()


            user1 = User(first_name = "Joe", last_name = "Jonas")
            db.session.add(user1)
            db.session.commit()

            self.user1_id = user1.id

            post1 = Post(title = "Hello There", content = "So excited to make my first post on Belytha's website!", user_id = user1.id)
            db.session.add(post1)
            db.session.commit()
            self.post1_id = post1.id
    
    def tearDown(self):
        """Cleans up any failing transactions"""
        with app.app_context():
            db.session.rollback()

    def test_show_post_on_user_page(self):
        """Show post on Joe Jonas user page"""
        res = self.client.get(f'/users/{self.user1_id}')
        html = res.get_data(as_text=True)

        self.assertIn('<h1>Joe Jonas</h1>', html)
        self.assertIn('<h2>Posts</h2>', html)
        self.assertIn('<li>Hello There</li>', html)

    def test_show_post_page(self):
        """Shows post page"""
        res = self.client.get(f'/posts/{self.post1_id}')
        html = res.get_data(as_text=True)

        self.assertIn("<h1>Hello There</h1>", html)
        self.assertIn('<p>By: Joe Jonas,', html)

    def test_show_edit_post(self):
        """Shows edit post page"""
        res = self.client.get(f'/posts/{self.post1_id}/edit')
        html = res.get_data(as_text=True)

        self.assertIn('<h1>Edit Post</h1>', html)
        self.assertIn('<label>Title:', html)







