import flask


def member_get(memberid=None, surname=None, addressline1=None, county=None, postcode=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(
            """SELECT
                memberid,
                title,
                forename,
                surname,
                companyname,
                addressline1,
                addressline2,
                city,
                county,
                country,
                postcode,
                homephone,
                mobilephone,
                dateofbirth
            FROM vw_member
            WHERE (%(memberid)s IS NULL or memberid = %(memberid)s)
              AND (%(surname)s IS NULL or surname LIKE %(surname)s)
              AND (%(addressline1)s IS NULL or addressline1 LIKE %(addressline1)s)
              AND (%(county)s IS NULL or county LIKE %(county)s)
              AND (%(postcode)s IS NULL or postcode LIKE %(postcode)s)
              OFFSET %(offset)s
              LIMIT %(limit)s""", {'memberid': memberid,
                                   'surname': surname,
                                   'addressline1': addressline1,
                                   'county': county,
                                   'postcode': postcode,
                                   'offset': offset,
                                   'limit': limit})

        queryresults = cur.fetchall()

        return queryresults


def member_create(entryuserid,
                  title,
                  forename,
                  surname,
                  addressline1,
                  addressline2,
                  city,
                  county,
                  country,
                  postcode,
                  homephone,
                  mobilephone,
                  dateofbirth,
                  companyname=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT member_create(%(title)s,
                                           %(forename)s,
                                           %(surname)s,
                                           %(companyname)s,
                                           %(addressline1)s,
                                           %(addressline2)s,
                                           %(city)s,
                                           %(county)s,
                                           %(country)s,
                                           %(postcode)s,
                                           %(homephone)s,
                                           %(mobilephone)s,
                                           %(dateofbirth)s,
                                           %(entryuserid)s)
                                           """, {'title': title,
                                                 'forename': forename,
                                                 'surname': surname,
                                                 'companyname': companyname,
                                                 'addressline1': addressline1,
                                                 'addressline2': addressline2,
                                                 'city': city,
                                                 'county': county,
                                                 'country': country,
                                                 'postcode': postcode,
                                                 'homephone': homephone,
                                                 'mobilephone': mobilephone,
                                                 'dateofbirth': dateofbirth,
                                                 'entryuserid': entryuserid})
        memberid = cur.fetchone()
        return memberid['member_create']


def member_update(memberid,
                  title,
                  forename,
                  surname,
                  companyname,
                  addressline1,
                  addressline2,
                  city,
                  county,
                  country,
                  postcode,
                  homephone,
                  mobilephone,
                  dateofbirth):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT member_update(
                                            %(memberid)s,
                                            %(title)s,
                                            %(forename)s,
                                            %(surname)s,
                                            %(companyname)s,
                                            %(addressline1)s,
                                            %(addressline2)s,
                                            %(City)s,
                                            %(County)s,
                                            %(Country)s,
                                            %(PostCode)s,
                                            %(HomePhone)s,
                                            %(MobilePhone)s,
                                            %(DateOfBirth)s
                                           )""", {'memberid': memberid,
                                                  'title': title,
                                                  'forename': forename,
                                                  'surname': surname,
                                                  'companyname': companyname,
                                                  'addressline1': addressline1,
                                                  'addressline2': addressline2,
                                                  'City': city,
                                                  'County': county,
                                                  'Country': country,
                                                  'PostCode': postcode,
                                                  'HomePhone': homephone,
                                                  'MobilePhone': mobilephone,
                                                  'DateOfBirth': dateofbirth,
                                                  })

