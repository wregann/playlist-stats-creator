from time import sleep
import mysql.connector as msc
import creds

if __name__ == "__main__":
    hourDiff = 1
    while True:
        try:
            mydb = msc.connection.MySQLConnection(user=creds.DB_USERNAME, password=creds.DB_PASSWORD,
                                    host=creds.DB_HOSTNAME,
                                    database='WeatherifyDB')
            mycursor = mydb.cursor()
            mycursor.execute("""DELETE FROM user_songs WHERE user_id IN 
                             (SELECT user_id FROM user_dates 
                             WHERE HOUR(TIMEDIFF(NOW(), datetime_accessed)) >= %s);""", [hourDiff])
            mycursor.execute("""DELETE FROM user_dates 
                             WHERE HOUR(TIMEDIFF(NOW(), datetime_accessed)) >= %s;""", [hourDiff])
            mydb.commit()
            mydb.close()
            
        except Exception as e:
            print(e)
            print("Error in connecting to databse")
            break
        
        # Wait an hour
        print("{0} Hour Old Users Cleared".format(hourDiff))
        sleep(3600)