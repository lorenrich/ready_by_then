'''
Create and alter events data
'''
def create_event(conn, 
                 name, 
                 event_date, 
                 num_adults, 
                 num_kids, 
                 will_kids_eat_adult_meal, 
                 dietary_needs,
                 event_complete,
                 notes):
    conn.execute(
        "INSERT INTO events (name, event_date, num_adults, num_kids, will_kids_eat_adult_meal, dietary_needs, event_complete, notes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, event_date, num_adults, num_kids, will_kids_eat_adult_meal, dietary_needs, event_complete, notes)
    )
    conn.commit()

    