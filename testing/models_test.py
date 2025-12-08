import pytest
from models import Episode, Guest, Appearance
from app import db

def test_episode_creation(client):
    with client.application.app_context():
        episode = Episode(date="5/22/03", number=42)
        db.session.add(episode)
        db.session.commit()
        
        assert episode.id is not None
        assert episode.date == "5/22/03"
        assert episode.number == 42

def test_guest_creation(client):
    with client.application.app_context():
        guest = Guest(name="Lena Thornton", occupation="illustrator")
        db.session.add(guest)
        db.session.commit()
        
        assert guest.id is not None
        assert guest.name == "Lena Thornton"
        assert guest.occupation == "illustrator"

def test_appearance_creation(client):
    with client.application.app_context():
        episode = Episode(date="6/10/03", number=43)
        guest = Guest(name="Kai Middleton", occupation="animator")
        db.session.add_all([episode, guest])
        db.session.commit()
        
        appearance = Appearance(rating=4, episode_id=episode.id, guest_id=guest.id)
        db.session.add(appearance)
        db.session.commit()
        
        assert appearance.id is not None
        assert appearance.rating == 4
        assert appearance.episode_id == episode.id
        assert appearance.guest_id == guest.id

def test_appearance_rating_validation(client):
    with client.application.app_context():
        episode = Episode.query.first()
        guest = Guest.query.first()
        
        valid_appearance = Appearance(rating=2, episode_id=episode.id, guest_id=guest.id)
        db.session.add(valid_appearance)
        db.session.commit()
        
        with pytest.raises(ValueError):
            invalid_appearance = Appearance(rating=11, episode_id=episode.id, guest_id=guest.id)
            db.session.add(invalid_appearance)
            db.session.commit()

def test_cascade_delete(client):
    with client.application.app_context():
        episode = Episode.query.first()
        episode_id = episode.id
        
        appearances_before = Appearance.query.filter_by(episode_id=episode_id).count()
        assert appearances_before > 0
        
        db.session.delete(episode)
        db.session.commit()
        
        appearances_after = Appearance.query.filter_by(episode_id=episode_id).count()
        assert appearances_after == 0
