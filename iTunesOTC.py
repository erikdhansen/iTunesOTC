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

sorted(l.songs, key = l.songs.__getitem__ )

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

  api_call = dispatch_table[d['op'][0]];

  if api_call == None:
      print("Unknown API Call %s" % d['op'][0])
      status = '405 Invalid Request'
  else:
    status = api_call(d)

  print("Returning status: %s" % status)
  return status


def list_songs_from(name):
  print("Listing all songs starting from %s" % name)

def find_song(d):
  key_name  = d['key_name'][0]
  key_value = d['key_value'][0]

  try:
    key_value = int(key_value)
    print("Key[%s] => %d IS an int" % key_name, key_value)
  except ValueError:
    print("Key[", key_name,"] => ", key_value ," is NOT an int")

  if key_name == 'id':
    return find_by_id(key_value)
  else:
    return find_by_key(key_name, key_value)


def find_by_id(id):
  print("Looking for id=%d" % id)
  for song_id, song in l.songs.items():
    if song_id == id:
      return song

def find_by_key(key_name, key_value):
  print 'Looking for {key_name} = {key_value}'.format(key_name = key_name, key_value = key_value)
  for song_id, song in l.songs.items():
    if song[key_name] == key_value:
      return song

def play_song(d):
  song = find_song(d)
  print("Adding %s to OTC playlist" % song.name)

def stop_song(d):
  print("Stopping currently playing song")

dispatch_table = {
  'find_song': find_song,
  'play_song': play_song,
  'stop_song': stop_song
}

if __name__ == '__main__':
  server = make_server('0.0.0.0', port, app)
  server.serve_forever()


