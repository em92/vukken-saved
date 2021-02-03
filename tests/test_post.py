from types import GeneratorType
from vukken_saved.models import Post


def test_post_constructor_no_kwargs(my_repost_stalin_birth):
    post = Post(my_repost_stalin_birth)
    assert post.owner_id == 333794035
    assert post.id == 140
    assert post.raw == my_repost_stalin_birth


def test_post_copy_history(my_repost_stalin_birth):
    post = Post(my_repost_stalin_birth)
    history_generator = post.extract_copy_history()
    assert isinstance(history_generator, GeneratorType)

    history_items = list(history_generator)
    assert len(history_items) == 2

    assert history_items[0].owner_id == -72028042
    assert history_items[0].id == 4742
    assert history_items[0].raw == my_repost_stalin_birth["copy_history"][0]

    assert history_items[1].owner_id == -134065160
    assert history_items[1].id == 25062
    assert history_items[1].raw == my_repost_stalin_birth["copy_history"][1]
