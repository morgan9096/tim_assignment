import allure
import pytest
import requests


_POST_IDS_RANGE = range(1, 100+1)
_CREATE_POST_RESPONSE_CODE = 201


@pytest.fixture(scope='module')
def posts_url(url_for_test: str) -> str:
    return f'{url_for_test}/posts'


def test_post_ids(posts_url: str, user_id: int):
    """
    Using this userID, fetch the user’s associated posts
     and verify they contain valid Post IDs
    (an integer between 1 and 100).
    """
    with allure.step(f'Getting posts data from {posts_url}'):
        response = requests.get(posts_url)
        assert response.ok
        all_posts = response.json()
        assert all_posts
    with allure.step(f'Filtering posts for userId={user_id}'):
        user_posts = [post for post in all_posts if post.get('userId') == user_id]
        assert user_posts

    for index, post in enumerate(user_posts, 1):
        post_id = post.get('id', 'None')
        with allure.step(f'User_id={user_id}. Checking post {index}/{len(user_posts)}'):
            fail_msg = f'Invalid post_id={post_id} for user_id={user_id}'
            assert post_id in range(1, 100 + 1), fail_msg


def test_make_post(posts_url: str, user_id: int):
    """
    Make a post using the same userID with a non-empty title and body,
      verify the correct
      response is returned (since this is a mock API,
      it might not return a Response code 200, so check the documentation).
    """
    post_title = 'foo'
    post_body = 'bar'
    payload = {'title': post_title, 'body': post_body, 'userId': user_id}
    with allure.step(f'User_id={user_id}.Send request to create a post'):
        response = requests.post(posts_url, data=payload)
        assert response.status_code == _CREATE_POST_RESPONSE_CODE
        post = response.json()
        assert post
    with allure.step(f'User_id={user_id}.Check create post response'):
        assert post['title'] == post_title
        assert post['body'] == post_body
        assert int(post['userId']) == user_id
