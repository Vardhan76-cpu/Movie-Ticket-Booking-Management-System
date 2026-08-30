from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import sqlite3, uuid, qrcode

BASE = Path(__file__).resolve().parent.parent
DB = BASE/"data"/"movie_booking.db"
TICKETS = BASE/"tickets"
FRONTEND = BASE/"frontend"
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
CORS(app)
TICKETS.mkdir(exist_ok=True)

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON"); return c

def init():
    c=db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,language TEXT,genre TEXT,duration TEXT);
    CREATE TABLE IF NOT EXISTS theatres(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,location TEXT);
    CREATE TABLE IF NOT EXISTS shows(id INTEGER PRIMARY KEY AUTOINCREMENT,movie_id INTEGER,theatre_id INTEGER,show_date TEXT,show_time TEXT,total_seats INTEGER,available_seats INTEGER,ticket_price REAL,show_type TEXT DEFAULT 'Regular',status TEXT DEFAULT 'Active',FOREIGN KEY(movie_id) REFERENCES movies(id),FOREIGN KEY(theatre_id) REFERENCES theatres(id));
    CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY AUTOINCREMENT,booking_id TEXT UNIQUE,customer_name TEXT,email TEXT,phone TEXT,show_id INTEGER,tickets INTEGER,total_cost REAL,status TEXT,created_at TEXT,FOREIGN KEY(show_id) REFERENCES shows(id));
    """)
    if c.execute("SELECT COUNT(*) FROM movies").fetchone()[0]==0:
        c.executemany("INSERT INTO movies(name,language,genre,duration) VALUES(?,?,?,?)",[
            ("Avatar: The Way of Water","English","Science Fiction","3h 12m"),
            ("Pushpa 2: The Rule","Telugu","Action","3h 20m"),
            ("Kalki 2898 AD","Telugu","Science Fiction","3h 1m"),
            ("RRR","Telugu","Action","3h 7m")])
        c.executemany("INSERT INTO theatres(name,location) VALUES(?,?)",[
            ("CineWave","Tirupati"),("Galaxy Cinemas","Tirupati"),("PVR Cinemas","Tirupati")])
        c.executemany("""INSERT INTO shows(movie_id,theatre_id,show_date,show_time,total_seats,available_seats,ticket_price,show_type)
                         VALUES(?,?,?,?,?,?,?,?)""",[
            (1,1,"2026-09-01","10:30",100,100,200,"Regular"),
            (1,1,"2026-09-01","19:00",100,100,250,"VIP"),
            (2,2,"2026-09-01","14:00",120,120,180,"Regular"),
            (2,2,"2026-09-01","20:00",120,120,220,"Special"),
            (3,3,"2026-09-02","18:30",150,150,200,"Regular"),
            (4,1,"2026-09-02","21:00",100,100,180,"VIP")])
    c.commit(); c.close()

@app.get("/")
def home(): return send_from_directory(FRONTEND,"index.html")

@app.get("/api/<kind>")
def lists(kind):
    c=db()
    if kind=="movies": q="SELECT * FROM movies ORDER BY name"
    elif kind=="theatres": q="SELECT * FROM theatres ORDER BY name"
    elif kind=="shows": q="""SELECT s.*,m.name movie_name,t.name theatre_name,t.location
        FROM shows s JOIN movies m ON m.id=s.movie_id JOIN theatres t ON t.id=s.theatre_id
        WHERE s.status='Active' ORDER BY s.show_date,s.show_time"""
    else: c.close(); return jsonify({"error":"Unknown endpoint"}),404
    rows=[dict(x) for x in c.execute(q).fetchall()]; c.close(); return jsonify(rows)

@app.post("/api/bookings")
def book():
    d=request.get_json(silent=True) or {}
    if not all(d.get(x) for x in ["customer_name","email","phone","show_id","tickets"]):
        return jsonify({"error":"All fields are required."}),400
    try: sid=int(d["show_id"]); n=int(d["tickets"])
    except: return jsonify({"error":"Invalid show or ticket count."}),400
    if not 1<=n<=10: return jsonify({"error":"Tickets must be between 1 and 10."}),400
    c=db()
    try:
        c.execute("BEGIN IMMEDIATE")
        s=c.execute("""SELECT s.*,m.name movie_name,t.name theatre_name,t.location FROM shows s
            JOIN movies m ON m.id=s.movie_id JOIN theatres t ON t.id=s.theatre_id
            WHERE s.id=? AND s.status='Active'""",(sid,)).fetchone()
        if not s: c.rollback(); return jsonify({"error":"Show not found."}),404
        if s["available_seats"]<n:
            c.rollback(); return jsonify({"error":"Not enough seats available.","available_seats":s["available_seats"]}),409
        bid="MTB-"+uuid.uuid4().hex[:8].upper(); total=n*s["ticket_price"]
        c.execute("UPDATE shows SET available_seats=available_seats-? WHERE id=?",(n,sid))
        c.execute("""INSERT INTO bookings(booking_id,customer_name,email,phone,show_id,tickets,total_cost,status,created_at)
                     VALUES(?,?,?,?,?,?,?,?,?)""",(bid,d["customer_name"],d["email"],d["phone"],sid,n,total,"Confirmed",datetime.now().isoformat(timespec="seconds")))
        c.commit()
        qfile=TICKETS/f"{bid}.png"
        qrcode.make(f"Booking: {bid}\nMovie: {s['movie_name']}\nShow: {s['show_date']} {s['show_time']}\nTickets: {n}").save(qfile)
        return jsonify({"booking_id":bid,"movie":s["movie_name"],"theatre":s["theatre_name"],"location":s["location"],
                        "show_date":s["show_date"],"show_time":s["show_time"],"tickets":n,"ticket_price":s["ticket_price"],
                        "total_cost":total,"status":"Confirmed","qr_url":f"/tickets/{qfile.name}"}),201
    except Exception as e:
        c.rollback(); return jsonify({"error":str(e)}),500
    finally: c.close()

@app.get("/api/bookings/<bid>")
def get_booking(bid):
    c=db(); r=c.execute("""SELECT b.*,m.name movie_name,t.name theatre_name,s.show_date,s.show_time
        FROM bookings b JOIN shows s ON s.id=b.show_id JOIN movies m ON m.id=s.movie_id JOIN theatres t ON t.id=s.theatre_id
        WHERE b.booking_id=?""",(bid,)).fetchone(); c.close()
    return (jsonify(dict(r)),200) if r else (jsonify({"error":"Booking not found"}),404)

@app.post("/api/bookings/<bid>/cancel")
def cancel(bid):
    c=db()
    try:
        c.execute("BEGIN IMMEDIATE"); b=c.execute("SELECT * FROM bookings WHERE booking_id=?",(bid,)).fetchone()
        if not b: c.rollback(); return jsonify({"error":"Booking not found"}),404
        if b["status"]=="Cancelled": c.rollback(); return jsonify({"error":"Already cancelled"}),409
        c.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=?",(bid,))
        c.execute("UPDATE shows SET available_seats=available_seats+? WHERE id=?",(b["tickets"],b["show_id"]))
        c.commit(); return jsonify({"message":"Booking cancelled","booking_id":bid})
    except Exception as e:
        c.rollback(); return jsonify({"error":str(e)}),500
    finally: c.close()

@app.get("/tickets/<path:name>")
def ticket(name): return send_from_directory(TICKETS,name)
@app.get("/api/health")
def health(): return jsonify({"status":"ok"})
init()
if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
