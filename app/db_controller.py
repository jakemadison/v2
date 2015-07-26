__author__ = 'Madison'

import sqlite3
from app import config
from app.generic_error import GenericError


def create_table():
    create_profile_table = '''CREATE TABLE IF NOT EXISTS user_profile
                          (profile_id INTEGER PRIMARY KEY asc, profilename text unique not NULL)'''

    create_events_table = '''CREATE TABLE IF NOT EXISTS events
                             (profile_id INTEGER, request_time date, ipr text, ufield text, pfield text, usertype text,
                             FOREIGN KEY(profile_id) REFERENCES user_profile(profile_id))'''

    conn = sqlite3.connect(config.DATABASE_LOC)  # when this is :memory:, dies immediately on execution finish.
    # conn.execute(create_statement)
    with conn:
        curr = conn.cursor()

        curr.execute(create_profile_table)
        curr.execute(create_events_table)

        conn.commit()


def get_profile_list():

    get_all_profiles = '''
      select user_profile.profilename, CASE WHEN events.profile_id is null THEN 0 ELSE count(*) END
      from user_profile
        left outer join events on user_profile.profile_id = events.profile_id
      group by 1;
    '''
    conn = sqlite3.connect(config.DATABASE_LOC)  # when this is :memory:, dies immediately on execution finish.
    with conn:
        curr = conn.cursor()
        curr.execute(get_all_profiles)
        results = curr.fetchall()
        #print results
        return results

def profile_exists(name):
    cmd = """select count(*) from user_profile where profilename=?"""
    conn = sqlite3.connect(config.DATABASE_LOC)  # when this is :memory:, dies immediately on execution finish.
    with conn:
        curr = conn.cursor()
        curr.execute(cmd, [name])
        db_results = curr.fetchall()
    return db_results[0][0] > 0

def get_profile_id(name):
    cmd = """select profile_id from user_profile where profilename=?"""
    conn = sqlite3.connect(config.DATABASE_LOC)  # when this is :memory:, dies immediately on execution finish.
    with conn:
        curr = conn.cursor()
        curr.execute(cmd, [name])
        db_results = curr.fetchall()
    return db_results[0][0]



def create_new_profile(name):
    # run get user list first, and make sure it's not in there
    if profile_exists(name):
        raise GenericError('Profile already exists')

    insert_profile = '''insert into user_profile (profilename) VALUES (?)'''

    conn = sqlite3.connect(config.DATABASE_LOC)  # when this is :memory:, dies immediately on execution finish.
    with conn:
        curr = conn.cursor()
        curr.execute(insert_profile, [name])
        conn.commit()


def insert_event(name, time, ipr, ufield, pfield, usertype):

    current_profiles = get_profile_list()

    if not profile_exists(name):
        raise GenericError('Profile does not exist')

    profile_id = get_profile_id(name)

    insert_event_statement = '''insert into events (profile_id, request_time, ipr, ufield, pfield, usertype)
                                VALUES (?,?,?,?,?,?);'''

    conn = sqlite3.connect(config.DATABASE_LOC)
    with conn:
        curr = conn.cursor()
        curr.execute(insert_event_statement, [profile_id, time, ipr, ufield, pfield, usertype])
        conn.commit()


def get_all_events():
    cmd = '''select u.profilename, e.request_time, e.ipr, e.ufield, e.pfield, e.usertype
             from user_profile u join events e on e.profile_id = u.profile_id
             order by request_time asc'''
    conn = sqlite3.connect(config.DATABASE_LOC)
    conn.row_factory= sqlite3.Row
    with conn:
        curr = conn.cursor()
        curr.execute(cmd)
        db_results = curr.fetchall()
    return db_results

def get_all_events_for_profile(name):

    get_events = '''select u.profilename, e.request_time, e.ipr, e.ufield, e.pfield
                    from user_profile u join events e on e.profile_id = u.profile_id
                    where u.profilename = ?'''

    conn = sqlite3.connect(config.DATABASE_LOC)
    with conn:
        curr = conn.cursor()
        curr.execute(get_events, [name])
        db_results = curr.fetchall()

    return db_results


if __name__ == '__main__':
    # create_table()

    res = get_all_events_for_profile('test2')

    for r in res:
        print r

    # print create_new_user('test_user3')
    # print insert_event('test_user2', 'time3', 'ipr dat1')
