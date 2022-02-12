#! encoding = utf-8

import sqlite3
from math import log, ceil
from datetime import datetime, date, timedelta
from dictionary import TENSE_MOODS, PERSONS


class AppDB:
    """ Application database object """

    def __init__(self, path):

        self._conn = sqlite3.connect(path)
        self._c = self._conn.cursor()
        create_tbls(self._conn, self._c)

    def num_expired_entries(self, enabled_tm_idx):
        enabled_idx_str = ','.join([str(i) for i in enabled_tm_idx])
        sql = """ SELECT COUNT(id) FROM practice_forward WHERE tense_mood_idx IN ({:s})
                    AND DATE(expiration_date, 'localtime') < '{:s}'
                """.format(enabled_idx_str, date.today().strftime('%Y-%m-%d'))
        self._c.execute(sql)
        n1 = self._c.fetchone()[0]
        sql = """ SELECT COUNT(id) FROM practice_backward WHERE tense_mood_idx IN ({:s})
                            AND DATE(expiration_date, 'localtime') < '{:s}'
                        """.format(enabled_idx_str, date.today().strftime('%Y-%m-%d'))
        self._c.execute(sql)
        n2 = self._c.fetchone()[0]
        return n1, n2

    def choose_verb(self, tbl, enabled_tm_idx):
        enabled_idx_str = ','.join([str(i) for i in enabled_tm_idx])
        sql = """ SELECT {0:s}.id, {0:s}.verb, explanation, tense_mood_idx, person_idx 
        FROM {0:s}
            JOIN glossary ON {0:s}.verb_id = glossary.id 
        WHERE
            tense_mood_idx IN ({1:s})
            AND DATE(expiration_date, 'localtime') < '{2:s}' 
        ORDER BY RANDOM() LIMIT 1
        """.format(tbl, enabled_idx_str, date.today().strftime('%Y-%m-%d'))
        self._c.execute(sql)
        return self._c.fetchone()

    def update_res(self, tbl, entry_id, is_correct):
        """ Update practice result
        :argument
            tbl: str            table name
            entry_id: int       entry id
            is_correct: bool    answer result
        """
        # get the current correct_num number
        self._c.execute("SELECT correct_num, DATE(expiration_date, 'localtime') "
                        "FROM {:s} WHERE id = (?)".format(tbl), (entry_id, ))
        n, d = self._c.fetchone()
        if is_correct:      # if this time is correct
            # if the previous correct num is positive, consecutive correct answers
            # enlong the expiration date to
            # 1. today, if the last expiration + add_date is still past
            # 2. the expected day, if last expiration + add_date is future
            new_expiration_date = datetime.strptime(d, '%Y-%m-%d') + timedelta(days=add_to_expiration_date(n))
            if new_expiration_date.date() < date.today():
                new_date = date.today()
            else:
                new_date = new_expiration_date.date()
            sql = """ UPDATE {:s} SET (correct_num, expiration_date) 
            = (?, ?) WHERE id = (?) """.format(tbl)
            self._c.execute(sql, (max(0, n)+1, new_date.strftime('%Y-%m-%d'), entry_id))
        else:               # if this time is wrong
            # in case of typo, check if last time is also wrong
            if n < -1:      # last time is already wrong, this means we need to refresh this verb
                # set expiration date immediately to today
                sql = """ UPDATE {:s} SET (correct_num, expiration_date) 
                = (?, ?) WHERE id = (?) """.format(tbl)
                self._c.execute(sql, (n-1, date.today().strftime('%Y-%m-%d'), entry_id))
            else:
                # last time is correct, then this time we don't reset the expiration date,
                # but we update the correct_num to -1
                sql = """ UPDATE {:s} SET correct_num = (?) 
                WHERE id = (?) """.format(tbl)
                self._c.execute(sql, (-1, entry_id))

    def check_exist(self, verb):
        """ Check if verb exists in glossary """
        sql = """SELECT COUNT(id) FROM glossary WHERE verb = (?)"""
        self._c.execute(sql, (verb,))
        return bool(self._c.fetchone()[0])

    def add_voc(self, verb, explanation):
        """ Add vocabulary to glossary table"""
        # add new word
        sql = """ INSERT INTO glossary (verb, explanation) VALUES (?, ?) """
        self._c.execute(sql, (verb, explanation))
        # get this verb id
        sql = """ SELECT id FROM glossary WHERE verb = (?) """
        self._c.execute(sql, (verb, ))
        verb_id = self._c.fetchone()[0]
        # insert into practice tables
        practice_tuple = list(
                (verb, verb_id, tm_i, p_i) for tm_i in range(len(TENSE_MOODS))
                for p_i in range(len(PERSONS)))
        sql = """ INSERT INTO {:s} (verb, verb_id, tense_mood_idx, person_idx) 
        VALUES (?, ?, ?, ?)"""
        for tbl in ('practice_forward', 'practice_backward'):
            self._c.executemany(sql.format(tbl), practice_tuple)
        self._conn.commit()

    def update_voc(self, verb, explanation):
        """ Update vocabulary explanation to glossary table"""
        sql = """ UPDATE glossary SET explanation = (?) WHERE verb = (?) """
        self._c.execute(sql, (explanation, verb))
        self._conn.commit()

    def get_explanation(self, verb):
        sql = """ SELECT explanation FROM glossary WHERE verb = (?) """
        self._c.execute(sql, (verb,))
        res = self._c.fetchone()
        if res:
            return res[0]
        else:
            return ''

    def get_glossary(self):
        """ Return all records in glossary """
        self._c.execute("SELECT verb, explanation FROM glossary ORDER BY verb")
        return self._c.fetchall()

    def close(self):
        self._conn.close()


def create_tbls(conn, c):
    """ Create tables """

    # dictionary table
    sql = """ CREATE TABLE IF NOT EXISTS glossary (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        verb TEXT UNIQUE, 
        explanation TEXT);"""
    c.execute(sql)

    # forward practice table
    sql = """ CREATE TABLE IF NOT EXISTS practice_forward (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        verb TEXT,
        verb_id INTEGER,
        tense_mood_idx INTEGER,
        person_idx INTEGER,
        correct_num INTEGER DEFAULT 0,
        expiration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""
    c.execute(sql)

    # backward practice table
    sql = """ CREATE TABLE IF NOT EXISTS practice_backward (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            verb TEXT,
            verb_id INTEGER,
            tense_mood_idx INTEGER,
            person_idx INTEGER,
            correct_num INTEGER DEFAULT 0,
            expiration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    c.execute(sql)

    conn.commit()


def add_to_expiration_date(n):
    """ Return the expiration date to be added based on consecutive correct number
    This matches the memory curve.
    The memory curve is exponential decay, so we match the half life
    :argument
        n: int      number of consecutive correct answers
    :returns
        d: int      number of dates to be added
    """

    return max(0, ceil(log(2) * n))
