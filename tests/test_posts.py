from app import schema, models
import pytest

# def test_get_all_posts(authorized_user, test_post):
#     res= authorized_user.get('/posts/')
#     def validate(post):
#         return schema.PostOut(**post)
#     post_map = map(validate,res.json())
#     list(post_map)
#     assert res.status_code == 200
#     assert len(res.json()) == len(test_post)
#     # assert post_map[0].id == test_post[0].id
    
def test_unauthorize__user_get__all_posts(client , test_post):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorize__user_get__single_posts(client , test_post):
    res = client.get(f'/posts/{test_post[0].id}')
    assert res.status_code == 401
    

def test__authorized_user_get_posts_null(authorized_user , test_post):
    res =authorized_user.get('/posts/99')
    assert res.status_code == 404
    
def test__authorized_user_get_single_post(authorized_user , test_post):
    res =authorized_user.get(f'/posts/{test_post[0].id}')
    post = schema.PostOut(**res.json())
    # assert post.Post.id == test_post[0].id
    assert res.status_code == 200

@pytest.mark.parametrize('title, content, published',[
    ('some title', 'hello world', True),
    ('some title2', 'hello there', True), 
    ('some title3', 'hello people', True)
    ])
def test_create_post (authorized_user , test_post, test_user_d, title, content, published):
    res =authorized_user.post('/posts/', json=({'title':title, 'content':content, 'published':published}))
    created_post =schema.Post(**res.json())
    assert res.status_code ==201
    assert created_post.content ==content