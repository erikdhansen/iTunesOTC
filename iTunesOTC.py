#
# Python iTunes OTC Server
#
from pyItunes import *
from wsgiref.simple_server import *
from cgi import escape
from urlparse import parse_qs

port = 2180

l = Library("iTunes Music Library.xml")

i = 0
print("Loaded %d songs from library file" % len(l.songs))
print("Starting up iTunesOTC server on port %d" % port)

def app(environ, start_response):
  headers = [('Content-Type', 'text/plain')]
  if environ['REQUEST_METHOD'] == 'POST':
    status = '405 POST not supported'
  else:
    d = parse_qs(environ['QUERY_STRING'])
    status = process_command(d)
  start_response(status, headers)
  return ['Success\n']


def process_command(d):
  status = '200 OK'

  op = d['op'][0]
  id_type = d['id_type'][0]
  id = d['id'][0]

  if id_type == 'id':
    song = find_song_by_id(int(id))
  else:
    if id_type == 'name':
      song = find_song_by_name(id)
    else:
      print("Invalid id_type: %s" % id_type)
      status = '405 Invalid Request'

  if op == 'PLAY':
    play_song(song)
  else:
    if op == 'STOP':
      stop_song()
    else:
      print("Unknown OP=%s" % op)
  print("Returning status: %s" % status)
  return status

def find_song_by_id(id):
  print("Looking for id=%d" % id)
  for song_id, song in l.songs.items():
    if song_id == id:
      return song

def find_song_by_name(name):
  print("Looking for name=%s" % name)
  for song_id, song in l.songs.items():
    if song.name == name:
      return song

def play_song(song):
  print("Adding %s to OTC playlist" % song.name)

def stop_song():
  print("Stopping currently playing song")

if __name__ == '__main__':
  server = make_server('0.0.0.0', port, app)
  server.serve_forever()


