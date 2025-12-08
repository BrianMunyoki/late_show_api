from app import app, db, Episode, Guest, Appearance

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create episodes
        episodes = [
            Episode(date="2/10/95", number=1),
            Episode(date="1/07/96", number=2),
            Episode(date="1/4/92", number=3),
            Episode(date="2/07/91", number=4),
        ]

        # Create guests
        guests = [
            Guest(name="Hellen", occupation="actor"),
            Guest(name="Makasi", occupation="director"),
            Guest(name="Brian", occupation="producer"),
            Guest(name="Hildah", occupation="script writer"),
        ]

        # Add to session
        db.session.add_all(episodes)
        db.session.add_all(guests)
        db.session.commit()

        # Create appearances
        appearances = [
            Appearance(rating=4, episode_id=1, guest_id=1),
            Appearance(rating=5, episode_id=1, guest_id=2),
            Appearance(rating=3, episode_id=2, guest_id=3),
            Appearance(rating=5, episode_id=2, guest_id=4),
            Appearance(rating=4, episode_id=3, guest_id=1),
            Appearance(rating=2, episode_id=4, guest_id=2),
        ]

        db.session.add_all(appearances)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
