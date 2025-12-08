import sys, os
#__file__ represent /home/brianmuema/phase4_office/late_show_api/testing/conftest.py
#os.path.dirname(__file__) represents: /home/brianmuema/phase4_office/late_show_api/testing
# os.path.join(..., "..") "..“ means go up one directory level so it becomes: /home/brianmuema/phase4_office/late_show_api
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_PATH)

import pytest
from app import app, db
from models import Episode, Guest, Appearance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create unique test data
            episode1 = Episode(date="3/15/01", number=10)
            episode2 = Episode(date="4/22/01", number=11)
            
            guest1 = Guest(name="Alice Rivers", occupation="dancer")
            guest2 = Guest(name="Mark Holloway", occupation="magician")
            
            db.session.add_all([episode1, episode2, guest1, guest2])
            db.session.commit()
            
            # One appearance for episode1 and guest1
            appearance = Appearance(
                rating=4,
                episode_id=episode1.id,
                guest_id=guest1.id
            )
            db.session.add(appearance)
            db.session.commit()
            
        yield client
        
        with app.app_context():
            db.drop_all()
